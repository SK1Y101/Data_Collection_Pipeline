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

Additionally, if selenium grid is running, the ip can be passed into the scraper, as in `scraper = Scraper("0.0.0.0")`, and can be forced to try to connect first with `scraper = Scraper("0.0.0.0", forceRemote=True)`.

# Milestones

## Milestone 1
For this project, I have decided to scrape the NASA Exoplanet Catalog(ue)
(Yes, the incorrect spelling annoys me)

I'm currently doing my masters in astrophysics, and as part of my masters thesis, I am observing, locating, and modelling exoplanets [Project here by the way](https://sk1y101.github.io/projects/TransitProject/), so this seemed like a great opportunity to link two areas of interest together.
Also, this minimises the amount of time I need to spend looking for information for my masters thesis, as most of the base info is sat locally on my machine from the scraper running!

## Milestone 2
Technologies: Selenium 4

Why Selenium? It's basically the De-facto codebase for webscraping, with a rich documentation that makes programming a breeze. I had attempted to use requests and bs4, but ran into a tiny problem: my webpages aren't static. No biggie though, this scraper just became general purpose!

By this point, we had a scraper that could load the main exoplanets page, find elements needed, and could click on things. we're almost there with required features.

## Milestone 3
Technologies: UUID v4, JSON, Selenium 4

Now we have a fully feldged web scraper, capable of pulling any required text from any iven webpage. As part of this project, we want to locate images too, so we've implemented a quick function that can navigate iframes and will take screenshots. (This was primarilly motivated by the specific layout of the target website)

With all of the required data, we need a method of storage. Luckily, this is a long solved problem, and we can very simply use the python dictionary to JSON (Javascript Object Notation file) methodology. As we want to have this data stored in a database, we're also using UUID to create unique identifiers for each entry.

## Milestone 4
Technologies: unittest

This is where most of the documentation you've read came to be. Before then, the project was a mess of random code and loose notes, whereas now its a mess of semi-ordered code and semi-ordered loose notes.

We also wrote some unittests to ensure that methods were working as expected. some documentation on those is available soon™

## Milestone 5
Techonologies: Boto3 & AWS

Now we're in the realm of scalable storage: We want lots of data, but not lots of harddrives.

Luckily, amazon web service has s3, a scalable storage system that we can interact with programatically using the boto3 library.

## Milestone 6
With all of the previous parts together, now all we need to do is fire up the scraper and leave it to run for a little bit. a quick estimation gives around 10 hours for all 4940 exoplanets currently known, but with a speedier internet connection that'll come down.

## Milestone 7
Technologies: Docker, selenium grid

We've got a perfectly functional scraper. Lets break it in ways we didn't even know exist.

I know that I should appreciate docker, its an awesome way of abstracting a lot of code away from specific operating systems by containerising the application, it was a massive slog to get setup.
Apparently setting up docker should take 2 days. It took 2 weeks, and I'm pretty sure I've now seen every possible error message possible with the selenium/firefox/python/docker combination.

Now that it works, we can run the scraper remotely. Just fire up the standalone firefox instance, point the scraper at the remote IP, and watch everything trun. It's kinda cool when it all comes together.