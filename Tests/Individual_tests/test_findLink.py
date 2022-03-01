# python imports
import unittest, sys
from selenium.common.exceptions import NoSuchElementException

# Scraper class
try:
    # try to import our scraper class to test
    from ...source.Scraper import Scraper
except:
    # if that didn't work, add the source folder to the path for importing
    sys.path.append("source")
    from Scraper import Scraper

# test url to visit (Yes this is technically flaunting my own site)
test_url = "https://sk1y101.github.io/projects/"

# create the unit testing class for the Scraper.findLink() function
class TestScraperFindLink(unittest.TestCase):
    # code to be executed when the unit test begins
    def setUp(self):
        self.scraper = Scraper()

    # code to be executed on completion of the test
    def tearDown(self):
        self.scraper.close()

    # code to test the finding
    def test_FindLink(self):
        # ensure we were sent to the webpage
        self.assertEqual(self.scraper.navigate(test_url), test_url)
        # ensure that it finds an asset I know is there
        elem = self.scraper.find("div", "class", "grid-item")
        self.assertIsNotNone(elem)
        # ensure that it found the correct asset
        link = self.scraper.findLink(elem)
        # if the link was correct, it should be for the transit project
        self.assertEqual(link[0], "/projects/TransitProject/")


# if this is the top level code, run the single unit test
if __name__ == '__main__':
    # run the unit test (I like seeing lots of information, so we'll make the verbosity four)
    unittest.main(verbosity=4)
