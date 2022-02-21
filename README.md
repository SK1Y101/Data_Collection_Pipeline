# Data_Collection_Pipeline
In this lab, you'll implement an industry grade data collection pipeline that runs scalably in the cloud.

# Possible data sources
Used in this project: Exoplanet details from Nasa Exoplanet Catalogue

Used in your project: Any website you want!

# File structure
`Repo/`<br>
├ `Tests/`<br>
│  ├ `Individual_tests/`<br>
│  │  └ `A file for each individual test`<br>
│  ├ `full_test.py`<br>
│  └ `README.md for the Testing area`<br>
├ `source/`<br>
│  ├ `raw_data/`<br>
│  │  ├ `exoplanet_details/`<br>
│  │  │  └ `A folder for each exoplanet, containing images in png format, and details as a json`<br>
│  │  └ `exoplanet_links.json`<br>
│  ├ `Scraper/`<br>
│  │  └ `__init__.py`<br>
│  └ `scrape_for_exoplanets.py`<br>
├ `.gitignore`<br>
└ `README.md`<br>

# Usage
Contained within `source/Scraper` is the scraper class, which can be imported and used with:
```python
from Scraper import Scraper

scraper = Scraper()
```

The scraper class exposes 17 public methods that can be used to build a scraper application. An explanation for each mthod is found inside the `source` directory, with a link [Here](https://github.com/SK1Y101/Data_Collection_Pipeline/tree/main/source).