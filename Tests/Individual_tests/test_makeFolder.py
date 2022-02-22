# python imports
import unittest, sys, os

# Scraper class
try:
    # try to import our scraper class to test
    from ...source.Scraper import Scraper
except:
    # if that didn't work, add the source folder to the path for importing
    sys.path.append("source")
    from Scraper import Scraper

# the folder to create
folder = "Tests/Individual_tests/test_folder/"

# create the unit testing class for the Scraper.makeFolder() function
class TestScraperFolder(unittest.TestCase):
    # code to be executed when the unit test begins
    def setUp(self):
        self.scraper = Scraper()

    # code to be executed on completion of the test
    def tearDown(self):
        self.scraper.close()

    # code to test the navigation
    def test_makeFolder(self):
        # create a folder
        self.scraper.makeFolder(folder)
        # ensure the folder exists
        self.assertTrue(os.path.exists(folder))
        # and delete the folder once done
        os.rmdir(folder)

# if this is the top level code, run the single unit test
if __name__ == '__main__':
    # run the unit test (I like seeing lots of information, so we'll make the verbosity four)
    unittest.main(verbosity=4)