# python imports
import unittest, sys, os, json

# Scraper class
try:
    # try to import our scraper class to test
    from ...source.Scraper import Scraper
except:
    # if that didn't work, add the source folder to the path for importing
    sys.path.append("source")
    from Scraper import Scraper

# the json file to create
jsonFileName = "Tests/Individual_tests/testJson.json"

# create the unit testing class for the Scraper.loadJson() function
class TestScraperLoadJson(unittest.TestCase):
    # code to be executed when the unit test begins
    def setUp(self):
        self.scraper = Scraper()

    # code to be executed on completion of the test
    def tearDown(self):
        self.scraper.close()

    # code to test the navigation
    def test_loadjson(self):
        # create the dictionary
        test_dict = {"a":1, "b":2, "c":[1, 2, 3]}
        # save to a json file using the function
        self.scraper.saveJSON(jsonFileName, test_dict)
        # verify that the json file exists
        self.assertTrue(os.path.exists(jsonFileName))
        # now atempt to read the JSON file with the scraper class
        data = self.scraper.loadJSON(jsonFileName)
        # check that it was corrcet
        self.assertEqual(data, test_dict)
        # remove the file when done
        os.remove(jsonFileName)
        # check that it fails if nothing is passed
        self.assertRaises(TypeError, self.scraper.checkForFile)

# if this is the top level code, run the single unit test
if __name__ == '__main__':
    # run the unit test (I like seeing lots of information, so we'll make the verbosity four)
    unittest.main(verbosity=4)