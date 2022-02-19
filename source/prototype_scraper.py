# import required modules
# Web scraping
from importlib.metadata import files
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support import expected_conditions as EC

# Standard python
import time, os, json, uuid
from tqdm import trange
from random import random
from contextlib import contextmanager

# alse, because I prefer this function name
wait = time.sleep

## base scraper class
class Scraper:
    # initialisation 
    def __init__(self):
        # fetch the webdriver
        self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        self.actions = ActionChains(self.driver)
        self.filedir = ""
    
    # find multiple elements that match an xpath thingy
    def findAll(self, tagName="*", attribute=None, value=None, source=None):
        ''' Locate all child elements of the source that match the XPath attributes:
            xpath = //tagName[@attribute=value]
            The source will default to the page if a parent element is not given. '''
        # compile the xpath string
        xpath="//{}[@{}='{}']".format(tagName, attribute, value) if attribute else "//{}".format(tagName)
        # if a container element was not given, use the driver
        if not source:
            source = self.driver
        # search for the element
        elem = source.find_elements(By.XPATH, xpath)
        # and return it
        return elem
    
    # find an element using xpath details
    def find(self, tagName="*", attribute=None, value=None, source=None):
        ''' Locate the first child element of the source that matches the XPath attributes:
            xpath = //tagName[@attribute=value]
            The source will default to the page if a parent element is not given. '''
        # compile the xpath string
        xpath="//{}[@{}='{}']".format(tagName, attribute, value) if attribute else "//{}".format(tagName)
        # if a container element was not given, use the driver
        if not source:
            source = self.driver
        # search for the element
        elem = source.find_element(By.XPATH, xpath)
        # and return it
        return elem
    
    # return all links in an object
    def findLink(self, element):
        ''' Locate all child elements that specifically refer to links. '''
        # fetch all references to "href"
        tags = element.get_attribute("innerHTML").split("href")
        # fetch all links in the text
        links = [tag.replace("'", '"').split('"')[1] for tag in tags[1:]]
        # return the links, either as a list if multiple or singular if not
        if len(links) <= 1:
            return links[0]
        return links
    
    def waitUntilFound(self, tagName="*", attribute=None, value=None, source=None, timeout=10):
        ''' Functionally equivalent to "Scraper.find", but will wait until an element is loaded before returning
            timeout: The number of seconds to wait until the program will stop looking for an element. '''
        # compile the xpath string
        xpath="//{}[@{}='{}']".format(tagName, attribute, value) if attribute else "//{}".format(tagName)
        # fetch the element with a wait timeout
        elem = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        # and return the element
        return elem
 
    # navigate to a webpage
    def navigate(self, url):
        ''' Go to a specified url, with a random wait time to throw off bot detection. '''
        # go to the url
        self.driver.get(url)
        # wait for a bit for the page contents to load
        wait(0.5)
    
    # scroll to a certain part of the page
    def scroll(self, scroll_percent=0.1):
        ''' Will scroll to a certain percentage of the site height. '''
        self.driver.execute_script("window.scrollTo(0, {}*document.body.scrollHeight);".format(float(scroll_percent)))
    
    # fetch all the options in a selection box
    def selectbox(self, element):
        ''' Fetch the options given by a dropdown element, and return a function for selecting them. '''
        # fetch a reference to the selection box
        select = Select(element)
        # compile all of the options, and return a function to select one
        return [o.text for o in select.options], select.select_by_visible_text
    
    # locate a selection box
    def waitForSelectbox(self, attribute=None, value=None, source=None):
        # error counter
        error = 0
        # try to fetch the selection box three times
        while error < 3:
            try:
                # try to find the element
                selectElem = self.waitUntilFound("select", attribute, value, source)
                # convert to a selection box
                options, select_option = self.selectbox(selectElem)
                # select an option, so that we load things
                try:
                    select_option(options[-2])
                except:
                    select_option(options[0])
                # if nothing failed, return the elements
                return options, select_option
            # if we encountered a problem
            except Exception as e:
                # increment the error counter
                error+=1
                # and have a small delay before trying again
                wait(0.1)
        # raise the exception that occured
        raise e

    
    # type after clicking on an element
    def typeBox(self, element, query=""):
        ''' Type a query into an input box, with random keystroke times to circumvent any bot detection. '''
        # select the element
        element.click()
        # type the query with random keytype strokes and hit enter
        for x in query+Keys.ENTER:
            wait(random()*0.1 + 0.01)
            element.send_keys(x)

    # load an iframe element
    @contextmanager
    def loadIframe(self, elemName, source=None, timeout=None):
        ''' Load an iframe element, and close on completion. If a timeout is given, this function will wait for the element to load
            elem: the iframe element.'''
        # fetch the iframe
        if timeout:
            elem = self.waitUntilFound("iframe", "id", elemName, source, timeout)
        else:
            elem = self.find("iframe", "id", elemName, source)
        # fetch the url of the iframe element
        iframeUrl = elem.get_attribute("src")
        try:
            # open new tab
            self.driver.execute_script("window.open('');")
            # switch to new tab
            self.driver.switch_to.window(self.driver.window_handles[-1])
            # switch to the iframe url
            self.navigate(iframeUrl)
            # also yield the frame if needed
            yield iframeUrl
        # if anything goes wrong, or we're done
        finally:
            # close the current window
            self.driver.close()
            # and switch to the next oldest tab
            self.driver.switch_to.window(self.driver.window_handles[-1])
    
    # make a folder if it dosen't exist <<<--- This could probably be implemented better to be honest
    def makeFolder(self, loc):
        ''' Create any folders in "loc" that don't exist yet. '''
        # remove the filename from loc if it was given
        loc = os.path.split(loc)[0]
        # if the folder dosent exist
        if not os.path.exists(loc):
            # split the filepath by directory
            dirs = loc.split("/")
            # itterate backwards over the directory
            for x in range(len(dirs))[::-1]:
                # if this directory exists, break here
                if os.path.exists("/".join(dirs[:x])):
                    break
            # and now create all of the directories that didn't exist
            for y in range(x, len(dirs)):
                os.mkdir("/".join(dirs[:y+1]))

    # initialise the local storage location
    def localStorage(self, loc):
        ''' Point to a folder that the scraper will use to store/load data locally. '''
        # if the location was relative, prepend the current working directory
        if not os.path.isabs(loc):
            loc = (os.getcwd() + "/" + loc).replace("//", "/")
        # ensure the folder for this file exists
        self.makeFolder(loc)
        # set to the location
        self.filedir = loc
    
    # take a screenshot of the page and save to a location
    def screenshot(self, fileName, useLocalStorage=True):
        ''' Take a screenshot of the current page.
            location: the filepath to store the screenshot in.
            useLocalStorage: Will prepend the local storage directory to the filename if set to true. '''
        # prepend if wanted
        if useLocalStorage:
            # ensure we don't have odouble slasshes by mistake
            fileName = (self.filedir + "/" + fileName).replace("//", "/")
        # ensure the folder for this file exists
        self.makeFolder(fileName)
        # save this screenshot to the correct location
        self.driver.save_screenshot(fileName)
    
    # check if a file exists
    def checkForFile(self, fileName, stale_time=7, useLocalStorage=True):
        ''' Check if a file exists, and whether it will be considered stale.
            fileName: The filepath to the file.
            stale_time: The number of days this file should be younger than to not be considered stale.
            useLocalStorage: Will prepend the local storage directory to the filename if set to true. '''
        # prepend if wanted
        if useLocalStorage:
            # ensure we don't have odouble slasshes by mistake
            fileName = (self.filedir + "/" + fileName).replace("//", "/")
        # return nothing if the file doesnt exist
        if not os.path.exists(fileName):
            return None
        # return nothing if the file is stale
        if (time.time() - os.path.getmtime(fileName)) > stale_time*86400:
            return None
        # otherwise, return true
        return True
    
    # load data from a JSON file
    def loadJSON(self, fileName, stale_time=7, useLocalStorage=True):
        ''' Load data from a JSON File, returning it if not stale.
            fileName: The filepath to the JSON file.
            stale_time: The number of days this file should be younger than to not be considered stale.
            useLocalStorage: Will prepend the local storage directory to the filename if set to true. '''
        # check the file exists and isnt stale
        if not self.checkForFile(fileName, stale_time, useLocalStorage):
            return None
        # prepend if wanted
        if useLocalStorage:
            # ensure we don't have odouble slasshes by mistake
            fileName = (self.filedir + "/" + fileName).replace("//", "/")
        # otherwise, load the JSON as a dict and return it
        with open(fileName, "r") as f:
            data = json.load(f)
        # and return the data
        return data
    
    # save data to a json file
    def saveJSON(self, fileName, data, useLocalStorage=True):
        ''' Store data to a JSON file.
            fileName: the name of the JSON file to save to.
            data: the data to save
            useLocalStorage: Will prepend the local storage directory to the filename if set to true. '''
        # prepend if wanted
        if useLocalStorage:
            # ensure we don't have odouble slasshes by mistake
            fileName = (self.filedir + "/" + fileName).replace("//", "/")
        # ensure the folder for this file exists
        self.makeFolder(fileName)
        # open the file
        with open(fileName, "w") as f:
            # store in JSON with my prefered indentation
            json.dump(data, f, sort_keys=True, indent=4)

    # close the web page
    def close(self):
        ''' Quit the scraping process. '''
        self.driver.quit()

# search for a specific exoplanet using the scraper
def search_exoplanet(scraper, name):
    ''' Use the search feature to find the link for a specific exoplanet. '''
    # go to the webpage
    scraper.navigate("https://exoplanets.nasa.gov/discovery/exoplanet-catalog/")
    # type the name into the search box
    search_box = scraper.waitUntilFound("input", "id", "desktop_search_field")
    # type the exoplanet name
    scraper.typeBox(search_box, name)
    # search for the exoplanet link
    elem = scraper.find("li", "class", "display_name")
    # try to find the link in the element
    href = scraper.findInHTML(elem, "href")
    # and return the link for this exoplanet
    return "https://exoplanets.nasa.gov/"+href

# fetch all exoplanet links on the page
def fetch_exoplanet_links(scraper):
    ''' Use the NASA Site to return a dictionary of all exoplanet links. '''
    print("Fetching exoplanet links")
    # empty dictionary that stores reference information
    refs = dict()
    # look for how many pages of results there are
    page_total = scraper.waitUntilFound("span", "class", "total_pages").text
    # find a reference to the next page button to click when done
    next_page = scraper.find("a", "rel", "next")
    # and the total number of exoplanets to look for
    total_planets = scraper.waitUntilFound("span", "class", "total_results").text

    # show the current exoplanet index
    def get_start():
        return scraper.waitUntilFound("span", "class", "start_index").text
    sidx = _sidx = get_start()

    # now itterate on each page
    for x in trange(int(page_total)):
        # compile a list of all exoplanets on the page
        results_table = scraper.find("div", "id", "results")
        # fetch a reference to all exoplanets in the table
        for exoplanet in scraper.findAll("ul", "class", "exoplanet", results_table):
            # the link
            link = scraper.findLink(exoplanet)
            # the name is the final part of the link that isn't empty
            name = link.split("/")[-2]
            # ad to our ref dict
            refs[name] = {"link":"https://exoplanets.nasa.gov/"+link}
        # go to the next page
        next_page.click()
        # if we reached the end of the values, stop the loop
        if scraper.waitUntilFound("span", "class", "end_index").text == total_planets:
            continue
        # wait until the start index increases
        while sidx == _sidx:
            wait(0.1)
            _sidx = get_start()
        sidx = _sidx
    print("All exoplanet pages scraped")
    # and return the dict
    return refs

# locate all relevant information of an exoplanet on the page
def exoplanet_info(scraper, link):
    ''' Fetch all the required information for a given exoplanet link page. '''
    info = dict()
    # find the wysiwyd description
    description = scraper.find("p", source=scraper.find("div", "class", "wysiwyg_content")).text
    info["Description"] = description
    # fetch the information grid for this planet
    info_grid = scraper.waitUntilFound("table", "class", "information_grid")
    # fetch all table details
    results = scraper.findAll("tr", "class", "fact_row")
    # look through the table for the details
    for details in results:
        # some fact rows have multiple facts
        facts = scraper.findAll("div", "class", "value", details)
        names = scraper.findAll("div", "class", "title", details)
        # fetch the values, removing empty
        facts = [fact.text for fact in facts if fact.text != ""]
        names = [name.text for name in names if name.text != ""]
        # zip the fact name, and the fact value together
        for name, fact in zip(names, facts):
            # and store them in our dictionary
            info[name.title()] = fact.replace("\n", " ")
    # return the planet information
    return info

# fetch exoplanet images
def fetch_exoplanet_images(scraper, planet_dict, data_location):
    ''' Navigate an exoplanet page and take screenshots of the interactive artists element as images.
        planet_dict: the dictionary of planetary details to be saved, see "generate_details". '''
    # blank image references dictionary
    images = dict()
    # switch to the iframe, with a timeout for loading
    with scraper.loadIframe("exo_pioneer_module", timeout=10) as iframeUrl:
        # store the ifram url in the image references
        images["Link"] = iframeUrl
        # fetch the dropdown section
        planetDropdown = scraper.waitUntilFound("div", "id", "dropUpId")
        # start the image id at zero
        imageId = 0
        # fetch the comparison dropdown
        options, select_option = scraper.waitForSelectbox("class", "dropdownInfo")
        # give it a second to load the image
        wait(1)
        # itterate on the options backwards (Jupiter, Earth, self)
        for option in options[::-1]:
            # select this comparison
            select_option(option)
            # wait for this to load
            wait(1)
            # local filepath for this image
            imageLink = "{}/images/{}.png".format(data_location, imageId)
            # take a screenshot of this option
            scraper.screenshot(imageLink)
            # and fetch the description for this image. (compare, compare to earth, compare to jupiter).
            description = option.replace("COMPARE TO", "COMPARISON WITH") if "TO" in option else planet_dict["Name"]
            # store a reference to this image in the dict
            images[str(imageId)] = {"Path": imageLink,
                                    "Description": description.capitalize(),}
            # increment the image id
            imageId += 1
    # add the images to the dictionary
    planet_dict["images"] = images
    # and return the dictionary
    return planet_dict

def generate_details(scraper, ref, fileStore="", stale_time=7):
    ''' Convert a dictionary of links into a dictionary of exoplanet information.
        scraper: an instance of the Scraper class to be used to fetch information.
        ref: a dictionary of links to the relevant page.
        fileStore: the directory for which each exoplanet information will be saved to.
        stale_time: the time to consider this file stale, see "Scraper.loadJson" for details. '''
    # fetch a list of references to search
    planets = list(ref.keys())
    # for every reference in the dictionary
    for x in trange(len(planets)):
        # fetch this planet reference
        name = planets[x]
        link = ref[name]["link"]
        # get the folder for this exoplanet
        data_loc = "{}/{}".format(fileStore, name.replace(" ", "_"))
        # check if this exoplanet has information already
        old_details = scraper.loadJSON(data_loc+"/details.json", stale_time)
        # if this exoplanet hasn't previously been searhed
        if not old_details:
            # use the name as an id, generate a uuid from it, and create the dictionary for this planet from that
            thisplanet = {"Id": name, "Uuid": str(uuid.uuid4()), "Link": link, "Name": name,}
            # navigate to the page
            scraper.navigate(link)
            # fetch the details for this planet too
            info = exoplanet_info(scraper, link)
            # and combine the info with this planets details
            thisplanet = {**thisplanet, **info}
        # otherwise, use the previously generated details
        else:
            thisplanet = old_details
        # check for images
        if not scraper.checkForFile(data_loc+"/images/0.png"):
            # fetch them if it didn't work
            thisplanet = fetch_exoplanet_images(scraper, thisplanet, data_loc)
        # save the details <<<--- Probably modify this if it ends up being too slow
        scraper.saveJSON(data_loc+"/details.json", thisplanet)
        # wait for a small amount of time

# main program loop
def main():
    ''' Main program loop, Will scrape for exoplanet information. '''
    # Try using it on the initial website!
    # create the scraper instance
    scraper = Scraper()

    # initialise the scraper storage location
    scraper.localStorage("source/raw_data")

    # navigate to the exoplanet page
    scraper.navigate("https://exoplanets.nasa.gov/discovery/exoplanet-catalog/")

    # expand the exoplanets table to the maximum
    per_page = scraper.waitUntilFound("select", "id", "per_page")
    # fetch the selection box
    options, select_func = scraper.selectbox(per_page)
    # select the max
    select_func(max(options))
    # and click
    per_page.click()
    # wait for it to change
    wait(1)
    # scroll down slightly
    scraper.scroll(0.1)
    
    # search for a locally stored links dictionary
    refs = scraper.loadJSON("exoplanet_links.json", 7)
    # otherwise, fetch manually
    refs = refs if refs else fetch_exoplanet_links(scraper)
    # store the links again
    scraper.saveJSON("exoplanet_links.json", refs)
    
    # generate the details for each planet, and pass in the local storage location
    generate_details(scraper, refs, "exoplanet_details", 7)
    
    # and close the scraping session
    scraper.close()

# only execute if this is the top level code
if __name__ == "__main__":
    # execute
    main()