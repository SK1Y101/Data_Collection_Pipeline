# python image
FROM python:3.8

# copy files
COPY . .

# update packages
RUN apt-get update

# install firefox, and pip
RUN apt-get install -y firefox-esr

# update pip and install packages
RUN pip install --upgrade pip && pip install -r requirements.txt

# run the scraper script
ENTRYPOINT ["python3", "scrape_for_exoplanets.py"]