# python imports
import unittest, sys

# Scraper class
try:
    # try to import our scraper class to test
    from ...source.Scraper import Scraper
except:
    # if that didn't work, add the source folder to the path for importing
    sys.path.append("source")
    from Scraper import Scraper

# test url to visit (Yes this is technically flaunting my own site)
test_url = "https://sk1y101.github.io/"

# create the unit testing class for the Scraper.navigate() function
class TestScraperNavigation(unittest.TestCase):
    # code to be executed when the unit test begins
    def setUp(self):
        self.scraper = Scraper()

    # code to be executed on completion of the test
    def tearDown(self):
        self.scraper.close()

    # code to test the navigation
    def test_navigate(self):
        # ensure we were sent to the webpage
        self.assertEqual(self.scraper.navigate(test_url), test_url)
        # ensure that it fails if nothinig is passed
        self.assertRaises(TypeError, self.scraper.navigate)

# if this is the top level code, run the single unit test
if __name__ == '__main__':
    # run the unit test (I like seeing lots of information, so we'll make the verbosity four)
    unittest.main(verbosity=4)