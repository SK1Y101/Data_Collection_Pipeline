# import required modules
# Web scraping
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# drivers for selenium
from webdriver_manager.firefox import GeckoDriverManager

# Standard python
import time, os, json
from random import random
from contextlib import contextmanager

# alse, because I prefer this function name
wait = time.sleep

## base scraper class
class Scraper:
    # initialisation 
    def __init__(self, address=None, headless=None, debugFlag=None):
        # try to use the local webdriver
        self.debugFlag = debugFlag
        self.__fetchDriver__(address=address, headless=headless)
        self.driver.maximize_window()
        self.actions = ActionChains(self.driver)
        self.filedir = ""
        self.debugFlag = debugFlag
    
    # fetch the selenium driver according to priority
    def __fetchDriver__(self, address=None, headless=None):
        # fetch the options for firefox
        options = webdriver.FirefoxOptions()
        # set to headless if desired
        if headless:
            options.headless = True
        
        # if an address was given, connect
        if address:
            # start the remote webdriver
            self.debug("Attempting to connect to remote driver")
            self.driver = webdriver.Remote(command_executor="http://{}".format(address), options=options)
            print("Connected to remote WebDriver.")
        # otherwise, local driver
        else:
            self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
    
    def debug(self, *value):
        if self.debugFlag:
            print(*value)

    # find multiple elements that match an xpath thingy
    def findAll(self, tagName="*", attribute=None, value=None, source=None):
        ''' Locate all child elements of the source that match the XPath attributes:
            xpath = //tagName[@attribute=value]
            The source will default to the page if a parent element is not given. '''
        # compile the xpath string
        xpath="//{}[@{}='{}']".format(tagName, attribute, value) if attribute else "//{}".format(tagName)
        self.debug("xpath for findall:", xpath)
        # if a container element was not given, use the driver
        if not source:
            source = self.driver
        # search for the element
        elem = source.find_elements(By.XPATH, xpath)
        self.debug("Elements located:", elem)
        # and return it
        return elem
    
    # find an element using xpath details
    def find(self, tagName="*", attribute=None, value=None, source=None):
        ''' Locate the first child element of the source that matches the XPath attributes:
            xpath = //tagName[@attribute=value]
            The source will default to the page if a parent element is not given. '''
        # compile the xpath string
        xpath="//{}[@{}='{}']".format(tagName, attribute, value) if attribute else "//{}".format(tagName)
        self.debug("Xpath for find:", xpath)
        # if a container element was not given, use the driver
        if not source:
            source = self.driver
        # search for the element
        elem = source.find_element(By.XPATH, xpath)
        self.debug("Element found:", elem)
        # and return it
        return elem
    
    # return all links in an object
    def findLink(self, element):
        ''' Locate all child elements that specifically refer to links, and return those links. '''
        # fetch all references to "href"
        tags = element.get_attribute("innerHTML").split("href")
        self.debug("Located tags for findlink:", tags)
        # fetch all links in the text
        links = [tag.replace("'", '"').split('"')[1] for tag in tags[1:]]
        self.debug("Located links:", links)
        # return the links, either as a list if multiple or singular if not
        return links
    
    def waitUntilFound(self, tagName="*", attribute=None, value=None, source=None, timeout=10):
        ''' Functionally equivalent to "Scraper.find", but will wait until an element is loaded before returning
            timeout: The number of seconds to wait until the program will stop looking for an element. '''
        # compile the xpath string
        xpath="//{}[@{}='{}']".format(tagName, attribute, value) if attribute else "//{}".format(tagName)
        self.debug("Xpath for finding:", xpath)
        # fetch the element with a wait timeout
        elem = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        self.debug("Located element:", elem)
        # and return the element
        return elem
 
    # navigate to a webpage
    def navigate(self, url):
        ''' Go to a specified url, with a random wait time to throw off bot detection. '''
        # go to the url
        self.debug("Url to navigate to:", url)
        self.driver.get(url)
        self.debug("Pointed to URL, Waiting")
        # wait for a bit for the page contents to load
        wait(0.5)
        # retrun the URL
        return self.driver.current_url
    
    # scroll to a certain part of the page
    def scroll(self, scroll_percent=0.1):
        ''' Will scroll to a certain percentage of the site height. '''
        self.debug("Scroll percentage:", float(scroll_percent))
        self.driver.execute_script("window.scrollTo(0, {}*document.body.scrollHeight);".format(float(scroll_percent)))
        # return the scroll percentage
        self.debug("Fetching scroll")
        scroll_px = self.driver.execute_script("return document.documentElement.scrollHeight")
        page_height = self.driver.execute_script("return document.body.scrollTop || document.documentElement.scrollTop")
        self.debug("Scroll px:", scroll_px, "\nPage height:", page_height)
        return float(page_height / scroll_px)
    
    # fetch all the options in a selection box
    def selectbox(self, element):
        ''' Fetch the options given by a dropdown element, and return a function for selecting them. '''
        # fetch a reference to the selection box
        self.debug("Element to select in", element)
        select = Select(element)
        self.debug("Select options:", select.options)
        # compile all of the options, and return a function to select one
        return [o.text for o in select.options], select.select_by_visible_text
    
    # locate a selection box
    def waitForSelectbox(self, attribute=None, value=None, source=None):
        # error counter
        error = 0
        self.debug("Waiting for selectbox")
        # try to fetch the selection box three times
        while error < 3:
            try:
                self.debug("Attempt", error)
                # try to find the element
                selectElem = self.waitUntilFound("select", attribute, value, source)
                # convert to a selection box
                options, select_option = self.selectbox(selectElem)
                # select an option, so that we load things
                try:
                    select_option(options[-2])
                except:
                    select_option(options[0])
                self.debug("Located select box")
                # if nothing failed, return the elements
                return options, select_option
            # if we encountered a problem
            except Exception as e:
                self.debug("error:",e)
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
        self.debug("Searching for typeable box in elem:", element)
        element.click()
        # type the query with random keytype strokes and hit enter
        self.debug("Typing:", query+"[Enter]")
        for x in query+Keys.ENTER:
            wait(random()*0.1 + 0.01)
            element.send_keys(x)

    # load an iframe element
    @contextmanager
    def loadIframe(self, elemName, source=None, timeout=None):
        ''' Load an iframe element, and close on completion. If a timeout is given, this function will wait for the element to load
            elem: the iframe element.'''
        # fetch the iframe
        self.debug("Locating iframe")
        if timeout:
            elem = self.waitUntilFound("iframe", "id", elemName, source, timeout)
        else:
            elem = self.find("iframe", "id", elemName, source)
        self.debug("found iframe element:", elem)
        # fetch the url of the iframe element
        iframeUrl = elem.get_attribute("src")
        try:
            self.debug("IFrame URL:", iframeUrl, "\nAttempting to open")
            # open new tab
            self.driver.execute_script("window.open('');")
            self.debug("Opened new tab for iframe")
            # switch to new tab
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.debug("Switched to new tab")
            # switch to the iframe url
            self.navigate(iframeUrl)
            self.debug("Scraping in iframe element")
            # also yield the frame if needed
            yield iframeUrl
        # if anything goes wrong, or we're done
        finally:
            self.debug("Closing iframe element")
            # close the current window
            self.driver.close()
            self.debug("Switching back to previous focus")
            # and switch to the next oldest tab
            self.driver.switch_to.window(self.driver.window_handles[-1])
    
    # make a folder if it dosen't exist <<<--- This could probably be implemented better to be honest
    def makeFolder(self, loc):
        ''' Create any folders in "loc" that don't exist yet. '''
        # remove the filename from loc if it was given
        loc = os.path.split(loc)[0]
        self.debug("checking folder exists at:", loc)
        # if the folder dosent exist
        if not os.path.exists(loc):
            self.debug("Folder {} did not exist, creating".format(loc))
            # split the filepath by directory
            dirs = loc.split("/")
            # itterate backwards over the directory
            for x in range(len(dirs))[::-1]:
                self.debug("checking if {} exists".format("/".join(dirs[:x])))
                # if this directory exists, break here
                if os.path.exists("/".join(dirs[:x])):
                    break
            self.debug("Searched all directories in path")
            # and now create all of the directories that didn't exist
            for y in range(x, len(dirs)):
                try:
                    self.debug("creating directory:", "/".join(dirs[:y+1]))
                    os.mkdir("/".join(dirs[:y+1]))
                except:
                    pass
            self.debug("Created all directories in path")
        # return the folder existing
        return os.path.exists(os.path.split(loc)[0])

    # initialise the local storage location
    def localStorage(self, loc):
        ''' Point to a folder that the scraper will use to store/load data locally. '''
        # if the location was relative, prepend the current working directory
        self.debug("setting local folder to:", loc)
        if not os.path.isabs(loc):
            loc = (os.getcwd() + "/" + loc).replace("//", "/")
        # ensure the folder for this file exists
        self.debug("checking for folder existance")
        self.makeFolder(loc)
        # set to the location
        self.debug("Set folder as local storage")
        self.filedir = loc
        # return the folder existing
        return os.path.exists(os.path.split(loc)[0])
    
    # prepend the local storage
    def __includeLocalStorage__(self, fileName, useLocalStorage=True):
        # split by any "/" markers
        fileName = fileName.split("/")
        # prepend the filedir if found
        if useLocalStorage and self.filedir:
            fileName.insert(0, self.filedir)
        # return the filename
        return "/".join(fileName)
    
    # take a screenshot of the page and save to a location
    def screenshot(self, fileName, useLocalStorage=True):
        ''' Take a screenshot of the current page.
            location: the filepath to store the screenshot in.
            useLocalStorage: Will prepend the local storage directory to the filename if set to true. '''
        # prepend if wanted
        fileName = self.__includeLocalStorage__(fileName, useLocalStorage)
        # ensure the folder for this file exists
        self.makeFolder(fileName)
        # save this screenshot to the correct location
        self.driver.save_screenshot(fileName)
        # return the file existing
        return os.path.exists(fileName)
    
    # check if a file exists
    def checkForFile(self, fileName, stale_time=7, useLocalStorage=True):
        ''' Check if a file exists, and whether it will be considered stale.
            fileName: The filepath to the file.
            stale_time: The number of days this file should be younger than to not be considered stale.
            useLocalStorage: Will prepend the local storage directory to the filename if set to true. '''
        # prepend if wanted
        fileName = self.__includeLocalStorage__(fileName, useLocalStorage)
        # return nothing if the file doesnt exist
        if not os.path.exists(fileName):
            return False
        # return nothing if the file is stale
        if (time.time() - os.path.getmtime(fileName)) > stale_time*86400:
            return False
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
        fileName = self.__includeLocalStorage__(fileName, useLocalStorage)
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
        fileName = self.__includeLocalStorage__(fileName, useLocalStorage)
        self.debug("Searching for json at", fileName)
        # ensure the folder for this file exists
        self.makeFolder(fileName)
        # open the file
        with open(fileName, "w") as f:
            # store in JSON with my prefered indentation
            json.dump(data, f, sort_keys=True, indent=4)
        # return 
        return True

    # close the web page
    def close(self):
        ''' Quit the scraping process. '''
        self.debug("Shutting down scraper")
        self.driver.quit()
        # return true if the driver closed
        return True