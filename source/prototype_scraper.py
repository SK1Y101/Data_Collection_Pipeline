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

# Standard python
import time, os, json, uuid
from random import random

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
 
    # navigate to a webpage
    def navigate(self, url):
        ''' Go to a specified url, with a random wait time to throw off bot detection. '''
        # go to the url
        self.driver.get(url)
        # wait for a random amount of time between 1 and 5 seconds so the site does not suspect we are a bot
        wait(random() * 4 + 1)
    
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
    
    # type after clicking on an element
    def typeBox(self, element, query=""):
        ''' Type a query into an input box, with random keystroke times to circumvent any bot detection. '''
        # select the element
        element.click()
        # type the query with random keytype strokes and hit enter
        for x in query+Keys.ENTER:
            wait(random()*0.1 + 0.01)
            element.send_keys(x)
    
    # initialise the local storage location
    def localStorage(self, loc):
        ''' Point to a folder that the scrap[er will use to store/load data locally. '''
        # if the location was relative, prepend the current working directory
        if not os.path.isabs(loc):
            loc = (os.getcwd() + "/" + loc).replace("//", "/")
        # if the directory doesnt exist
        if not os.path.exists(loc):
            # then create it
            os.mkdir(loc)
        # set to the location
        self.filedir = loc
    
    # load data from a JSON file
    def loadJSON(self, fileName, stale_time=7, useLocalStorage=True):
        ''' Load data from a JSON File, returning it if not stale.
            fileName: The filepath to the JSON file.
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
    search_box = scraper.find("input", "id", "desktop_search_field")
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
    page_total = scraper.find("span", "class", "total_pages").text
    # find a reference to the next page button to click when done
    next_page = scraper.find("a", "rel", "next")

    # now itterate on each page
    for x in range(int(page_total) - 1):
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
        # wait for the javascript to finish
        wait(1.5 + random())
    print("All exoplanet pages scraped")
    # and return the dict
    return refs

# locate all relevant information of an exoplanet on the page
def exoplanet_info(scraper, link):
    ''' Fetch all the required information for a given exoplanet link page. '''
    info = dict()
    # go to the webpage
    scraper.navigate(link)
    # find the wysiwyd description
    description = scraper.find("p", source=scraper.find("div", "class", "wysiwyg_content")).text
    # fetch the information grid for this planet
    info_grid = scraper.find("table", "class", "information_grid")
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

def generate_details(scraper, ref, fileStore="", stale_time=7):
    ''' Convert a dictionary of links into a dictionary of exoplanet information.
        scraper: an instance of the Scraper class to be used to fetch information.
        ref: a dictionary of links to the relevant page.
        fileStore: the directory for which each exoplanet information will be saved to.
        stale_time: the time to consider this file stale, see "Scraper.loadJson" for details. '''
    # blank output dictionary, and the previously generated details as a dict
    details = dict()
    # for every reference in the dictionary
    for key in ref:
        # fetch this planet reference
        name, link = key, ref[key]["link"]
        # use the name as an id, and generate a uuid from it
        details[key] = {"Id": name, "Uuid": str(uuid.uuid4()),}
        # check if this exoplanet has information already
        data_loc = fileStore+"/"+name.replace(" ", "_")
        old_details = scraper.loadJSON(data_loc, stale_time)
        # if this exoplanet hasn't previously been searhed
        if key not in old_details:
            # fetch the details for this planet too
            info = exoplanet_info(scraper, link)
            # and combine the info with this planets details
            details[key] = {**details[key], **info}
        # otherwise, use the previously generated details
        else:
            details[key] = old_details
        # save the details <<<--- Probably modify this if it ends up being too slow
        scraper.saveJSON(fileStore, details)
    # return the completed details dictionary
    return details

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
    per_page = scraper.find("select", "id", "per_page")
    # fetch the selection box
    options, select_func = scraper.selectbox(per_page)
    # select the max
    select_func(max(options))
    # and click
    per_page.click()
    # scroll down slightly
    scraper.scroll(0.1)
    
    # search for a locally stored links dictionary
    refs = scraper.loadJSON("exoplanet_links.json", 7)
    # otherwise, fetch manually
    refs = refs if refs else fetch_exoplanet_links(scraper)
    # store the links again
    scraper.saveJSON("exoplanet_links.json", refs)
    
    # generate the details for each planet, and pass in the local storage location
    exoplanet_details = generate_details(scraper, refs, "exoplanet_details", 7)
    
    # and close the scraping session
    scraper.close()

# only execute if this is the top level code
if __name__ == "__main__":
    main()