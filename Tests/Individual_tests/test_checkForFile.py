# python imports
import unittest, sys, os, time

# Scraper class
try:
    # try to import our scraper class to test
    from ...source.Scraper import Scraper
except:
    # if that didn't work, add the source folder to the path for importing
    sys.path.append("source")
    from Scraper import Scraper

# the folder to create
thisFile = "Tests/Individual_tests/test_checkForFile.py"
stale_time = 7

# create the unit testing class for the Scraper.checkForFile() function
class TestScraperFile(unittest.TestCase):
    # code to be executed when the unit test begins
    def setUp(self):
        self.scraper = Scraper()

    # code to be executed on completion of the test
    def tearDown(self):
        self.scraper.close()

    # code to test the navigation
    def test_checkForFile(self):
        # check the file exists
        exists = os.path.exists(thisFile)
        # check it isn't stale
        stale = (time.time() - os.path.getmtime(thisFile)) > stale_time*86400
        # and check both passed
        expectation = exists and not stale
        # show that expectation to the user I guess
        print("The file {} and is{} stale".format("exists"*exists + "doesn't exist"*(not exists), "n't"*(not stale)))
        # now check we had the expected behaviour
        self.assertEqual(self.scraper.checkForFile(thisFile, stale_time, False), expectation)
        # check that it fails if nothing is passed
        self.assertRaises(TypeError, self.scraper.checkForFile)

# if this is the top level code, run the single unit test
if __name__ == '__main__':
    # run the unit test (I like seeing lots of information, so we'll make the verbosity four)
    unittest.main(verbosity=4)