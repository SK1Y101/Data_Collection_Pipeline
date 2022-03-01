# Execute all unit tests for the scraper method
import unittest

# navigation
from Individual_tests.test_navigate import TestScraperNavigation
# scroll
from Individual_tests.test_scroll import TestScraperScroll

#loadIframe

# find
from Individual_tests.test_find import TestScraperFind

# findAll
from Individual_tests.test_findAll import TestScraperFindAll

# findLink
from Individual_tests.test_findLink import TestScraperFindLink

# waitUntilFound

# typeBox

# localStorage

# screenshot

# checkForFile
from Individual_tests.test_checkForFile import TestScraperFile

# makeFolder
from Individual_tests.test_makeFolder import TestScraperFolder

# loadJSON
from Individual_tests.test_loadJson import TestScraperLoadJson

# saveJSON
from Individual_tests.test_saveJson import TestScraperSaveJson

unittest.main(verbosity=4)