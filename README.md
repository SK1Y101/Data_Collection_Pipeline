# Data_Collection_Pipeline
In this lab, you'll implement an industry grade data collection pipeline that runs scalably in the cloud.

# Possible data sources
Exoplanet details

# File structure
`Repo/`
├─ `source/`
│  ├─ `raw_data/`
│  │  ├─ `exoplanet_details/`
│  │  │  └─ `A folder for each exoplanet, with the following format`
│  │  │     ├─ `images/`
│  │  │     │  └─ `Images aranged in numerical order`
│  │  │     └─ `details.json`
│  │  └─ `exoplanet_links.json`
│  ├─ `Scraper/`
│  │  └─ `__init__.py`
│  └─ `scrape_for_exoplanets.py`
├─ `.gitignore`
└─ `README.md`

# Usage
Contained within `source/Scraper` is the scraper class, which can be imported and used with:
```python
from Scraper import Scraper

scraper = Scraper()
```

The scraper class exposes the following 17 public methods that can be used to build a scraper application

### findAll
#### Explanation
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
</body>
```
Python
```python
elements = scraper.findAll("div", "class", "test_elements")

for element in elements:
    print(element.text)
```
Output
```
this is a test
this is also a test
```

### find
```python
Scraper.find(self, tagName="*", attribute=None, value=None, source=None)
```

### findLink
```python
Scraper.findLink(self, element)
```

### waitUntilFound

### navigate

### scroll

### selectbox

### waitForSelectbox

### typeBox

### loadIframe

### makeFolder

### localStorage

### screenshot

### checkForFile

### loadJSON

### saveJSON

### close