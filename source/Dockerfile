# python image
FROM python:3.8

# copy the scripts to run
COPY scrape_for_exoplanets.py \
     upload_to_aws.py \
     requirements.txt ./

# and the scraper class
COPY Scraper/ ./Scraper/

# update pip and install packages
RUN pip install --upgrade pip && pip install -r requirements.txt

# launch the selenium standalone instance


# run the scraper script
ENTRYPOINT ["python3", "scrape_for_exoplanets.py"]