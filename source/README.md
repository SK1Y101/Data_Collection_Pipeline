# Additional files in this directory

- `scrape_for_exoplanets.py` My own script utilising the `Scraper()` class to find data for exoplanets from the Nasa archive
- `raw_data\` a folder containing all of the scraped data from the above script

# Scraper Public Method Explanation

Each public mehod contains:
- Example method usage, with all arguments shown.
- Quick explanation of the functionality.
- And a Usage section that contains.
 - Example HTML Snippet if applicable.
 - Example Python script to show how one would use the function.
 - Output of the python script, if applicable.

## navigate
```python
Scraper.navigate(url)
```

The scraper will navigate to the desired url.

The scraper will also hold code execution until the webpage has loaded, such that following code can execute properly.

#### Example Usage
Python
```python
from Scraper import Scraper
scraper = Scraper()

scraper.navigate("www.google.com")
```

## close
```python
Scraper.close()
```

The scraper will close the current webpage. This behavior is usually used to shutdown the webdriver.

#### Example Usage
Python
```python
from Scraper import Scraper
scraper = Scraper()

scraper.navigate("www.google.com")
scraper.close()
```

## loadIframe
```python
Scraper.loadIframe(elemName, source=None, timeout=None):
```

Load an iframe element in a new tab, and close that tab upon completion. Used as part of a `with` statement, which will also yield the url of the iframe element.

elemName: the HTML Id of the iframe to open

source: the parent element to search. If this is not given, the code will search the entire page. (SEE: `Scraper.find()` for exlanation)

timeout: The amount of time to wait for this element to load and be found. If not given, the function will throw an error if the element cannot be immediately located. (SEE: `Scraper.waitUntilFound() for explanation`)

#### Example Usage
HTML
```HTML
<body>
    <div>
        <iframe id="wiki_iframe" src="https://www.wikipedia.org/"/>
    </div>
</body>
```
Python
```python
from Scraper import Scraper
scraper = Scraper()

with scraper.loadIframe("wiki_iframe", 3) as iframeUrl:
    # fetch the title from that page
    title = scraper.load("span", "class", "central-textlogo__image")
    print(title.text)
    print(iframeUrl)
```
Output
```
Wikipedia
https://www.wikipedia.org/
```

## scroll
```python
CODE
```

EXPLAIN

#### Example Usage
HTML
```HTML

```
Python
```python

```
Output
```

```

## find
```python
Scraper.find(tagName="*", attribute=None, value=None, source=None)
```

The scraper will locate the first element that matches the xpath string `//tagName[@attribute=value]`

tagName defines the HTML tag, ie: Div, Section, tr, ...

attribute defines an HTML attribute, ie: id, class, height, ...


if a source element is provided, the scraper will only search elements that are children of that element.

If one is not provided (default behavior of the method), then the scraper will find the first match in the entire page

#### Example Usage
HTML
```HTML
<body>
    <div id="test">
        <div class="test_elements">
            this is a test
        </div>
        <div class="test_elements">
            this is also a test
        </div>
    </div>
    <div class="test_elements">
        this element is not a child of 'test'
    </div>
</body>
```
Python
```python
from Scraper import Scraper
scraper = Scraper()

element = scraper.find("div", "class", "test_elements")

print(element.text)
```
Output
```
this is a test
```

## findAll
```python
Scraper.findAll(tagName="*", attribute=None, value=None, source=None)
```

The scraper will locate all elements that match the xpath string `//tagName[@attribute=value]`, and return them as a list

tagName defines the HTML tag, ie: Div, Section, tr, ...

attribute defines an HTML attribute, ie: id, class, height, ...


if a source element is provided, the scraper will only locate elements that are children of that element.

If one is not provided (default behavior of the method), then the scraper will find all matching elements on the current page

#### Example Usage
HTML
```HTML
<body>
    <div id="test">
        <div class="test_elements">
            this is a test
        </div>
        <div class="test_elements">
            this is also a test
        </div>
    </div>
    <div class="test_elements">
        this element is not a child of 'test'
    </div>
</body>
```
Python
```python
from Scraper import Scraper
scraper = Scraper()

elements = scraper.findAll("div", "class", "test_elements")

for element in elements:
    print(element.text)
```
Output
```
this is a test
this is also a test
this element is not a child of 'test'
```


## findLink
```python
Scraper.findLink(element)
```

Will locate all links within an element, this includes links found in child elements, and the element itself.

#### Example Usage
HTML
```HTML
<body>
    <a href="www.google.com">Google</a>
    <div id="store_links">
        <a href="https://github.com/SK1Y101/Data_Collection_Pipeline">This project!</a>
        <a href="https://github.com/SK1Y101/Computer-Vision-Rock-Paper-Scissors">The previous project!</a>
    </div>
</body>
```
Python
```python
from Scraper import Scraper
scraper = Scraper()

link_section = Scraper.find("div", "id", "store_links")

links = Scraper.findLinks(link_section)

for link in links:
    print(link)
```
Output
```
https://github.com/SK1Y101/Data_Collection_Pipeline
https://github.com/SK1Y101/Computer-Vision-Rock-Paper-Scissors
```


## waitUntilFound
```python
CODE
```

EXPLAIN

#### Example Usage
HTML
```HTML

```
Python
```python

```
Output
```

```

## selectbox
```python
CODE
```

EXPLAIN

#### Example Usage
HTML
```HTML

```
Python
```python

```
Output
```

```

## waitForSelectbox
```python
CODE
```

EXPLAIN

#### Example Usage
HTML
```HTML

```
Python
```python

```
Output
```

```

## typeBox
```python
CODE
```

EXPLAIN

#### Example Usage
HTML
```HTML

```
Python
```python

```
Output
```

```

## localStorage
```python
CODE
```

EXPLAIN

#### Example Usage
HTML
```HTML

```
Python
```python

```
Output
```

```

## screenshot
```python
CODE
```

EXPLAIN

#### Example Usage
HTML
```HTML

```
Python
```python

```
Output
```

```

## checkForFile
```python
CODE
```

EXPLAIN

#### Example Usage
HTML
```HTML

```
Python
```python

```
Output
```

```

## makeFolder
```python
CODE
```

EXPLAIN

#### Example Usage
HTML
```HTML

```
Python
```python

```
Output
```

```

## loadJSON
```python
CODE
```

EXPLAIN

#### Example Usage
HTML
```HTML

```
Python
```python

```
Output
```

```

## saveJSON
```python
CODE
```

EXPLAIN

#### Example Usage
HTML
```HTML

```
Python
```python

```
Output
```

```