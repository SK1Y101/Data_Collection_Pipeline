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
Technologies: Docker, selenium grid, EC2

We've got a perfectly functional scraper. Lets break it in ways we didn't even know exist.

### Running the scraper from a container

I know that I should appreciate docker, its an awesome way of abstracting a lot of code away from specific operating systems by containerising the application, but it was a massive slog to get setup. Apparently setting up a docker image for this project should take 2 days.

It took 3 weeks.

And I'm pretty sure I've now seen every possible error message possible with the selenium/firefox/python/docker combination.

Now that it works, we can run the scraper remotely. Just fire up the standalone firefox instance, point the scraper at the remote IP, and watch everything trun. It's kinda cool when it all comes together.

Now, to ensure that works, we need to be able to pass arguments to our python script (Specifically, the ip, port, and headless mode). We can quite simply achieve this, just change the CMD to an ENTRYPOINT in our Docker file, and pass the environment variables when we run the container!

The variables are `--address targetIp:targetPort`, which is the location of the selenium standalone instance for remote webscraping, `--headless`, which if included will enable headless webscraping, and `--upload`, which if included will upload all files to an AWS S3 bucket once the scraper is finished.

### Running the scraper in the cloud

Have you heard of EC2?

Me neither!

Lets get the scraper working in it.

## Milestone 8

Technologies: Docker, Prometheus, Grafana

We have a cloud based scraper, lets see how its doing

### Monitoring the Computer

We need to setup a prometheus docker instance to monitor the EC2 metrics, so we can see what's happeneing

To do this, we're using the Node Exporter library, which will be able to see things such as CPU usage and network movement (I think?)

### Monitoring the Scraper

We can see what the computer is doing with prometheus, we can see what the scraper is doing with selenium, let's combine them so we can see how the scraper is doing in prometheus!

### Dashboard

ToDo: GRAFANA

We have a Grafana dashboard for the EC2 Instance, now We just need one for the scraper and we're golden!

### Dashboard

## Milestone 9

Technologies: CI/CD, Cron

Lets automate the loose ends, now humans should only be needed for debuging, and developing. Not for deployment!

### Restarting

We made a quick script to shutdown the scraper at midnight, and then start it back up again a few seconds later. As a result of the implementation, we also restart selenium hub.

### Updating

During the downtime, the cron script searches for any updates to the docker scripts, updates that are automatically generated by a github action when a pull request is made to the main branch.

And with that, we have a fully functional, fully scalpable, and fully cloud based, exoplanet information scraper.

## Closing remarks

Selenium is great, *When it works*.

Unit testing is great, *Except they're really tedious and quite boring to write*.

Docker is great, *When you're not trying to integrate loads of things at once on quite literally your first time using docker*.

AWS is... acceptable. I don't know, I'm just not really a fan. The services worked well enough, I just didn't really like using it all that much.

GitHub is great. There is no "but" or "except". It's just great. 11/10. Will always use GitHub.

The project took a little longer than expected, but I suppose that was to be expected given my slightly unorthodox method (EC2 + Docker + Selenium Hub was a strange mix, but using Firefox rather than chrome just exacerbated the issues), and having to learn basically everything that wasn't python on the job.

The actual programming for the project was super easy and very enjoyable. Learning how to programatically interact with dynamic webpages was surprisingly fun. If I could convince someone else to deal with everything between milestone 4 and 8, I'd be happy to write another scraper. Until then, this will probably be another skill that I let sit idle for a while.