Unit testing area!

All of the unit tests for the public methods are found in the `Individual_tests` folder, with each file being named according to the public method it is testing.

Note: The public method `Scraper.close()` is required to cleanly shutdown the scraping class, and does not have it's own test, instead being called for every public method. If they do not throw any errors, then clearly the `Scraper.close()` works.

[x] navigate
- `/test_navigate.py`

[ ] loadIframe

[x] scroll

[ ] find

[ ] findAll

[ ] findLink

[ ] waitUntilFound

[ ] typeBox

[ ] localStorage

[ ] screenshot

[x] checkForFile

[x] makeFolder

[ ] loadJSON

[ ] saveJSON