# import required modules
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from webdriver_manager.firefox import GeckoDriverManager

from time import sleep as wait
from random import random

## base scraper class
class Scraper:
    # initialisation 
    def __init__(self):
        # fetch the webdriver
        self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        self.actions = ActionChains(self.driver)
    
    # find multiple elements that match an xpath thingy
    def findAll(self, tagName="*", attribute="id", value="", source=None):
        # compile the xpath string
        xpath="//{}[@{}='{}']".format(tagName, attribute, value)
        # if a container element was not given, use the driver
        if not source:
            source = self.driver
        # search for the element
        elem = source.find_elements(By.XPATH, xpath)
        # and return it
        return elem
    
    # find an element using xpath details
    def find(self, tagName="*", attribute="id", value="", source=None):
        # find the elements
        elems = self.findAll(tagName, attribute, value, source)
        # only return the first
        return elems
    
    # find given html
    def findInHTML(self, element, htmlsearch=""):
        # fetch the html of the element
        html = self.elementHTML(element)
        # and return the value found
        return html.split(htmlsearch)[1].replace("'", '"').split('"')[1]
 
    # navigate to a webpage
    def navigate(self, url):
        # go to the url
        self.driver.get(url)
        # wait for a random amount of time between 1 and 5 seconds so the site does not suspect we are a bot
        wait(random() * 4 + 1)
    
    # return the html of an element if that is useful
    def elementHTML(self, element):
        # return the HTML stuff
        return element.get_attribute("innerHTML")
    
    # fetch all the options in a selection box
    def selectbox(self, element):
        # fetch a reference to the selection box
        select = Select(element)
        # compile all of the options, and return a function to select one
        return [o.text for o in select.options], select.select_by_visible_text
    
    # type after clicking on an element
    def typeBox(self, element, query=""):
        # select the element
        element.click()
        # type the query with random keytype strokes and hit enter
        for x in query+Keys.ENTER:
            wait(random()*0.1 + 0.01)
            element.send_keys(x)

    # close the web page
    def close(self):
        self.driver.quit()

# search for a specific exoplanet using the scraper
def search_exoplanet(scraper, name):
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

# main program loop
def main():
    # source location
    # https://exoplanets.nasa.gov/discovery/exoplanet-catalog/
    # examples of query:
    #11 comae berenices b: https://exoplanets.nasa.gov/exoplanet-catalog/6988/11-comae-berenices-b/
    #HAT-P-44 bhttps://exoplanets.nasa.gov/exoplanet-catalog/1260/hat-p-44-b/

    # create the scraper instance
    scraper = Scraper()

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

    # compile a list of all exoplanets on the page
    results_table = scraper.find("div", "id", "results")
    # fetch a reference to all exoplanets in the table
    exoplanets = scraper.findAll("ul", "class", "exoplanet", results_table)

    print(exoplanets)

# only execute if this is the top level code
if __name__ == "__main__":
    main()