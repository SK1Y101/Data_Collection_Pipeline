# CronJobs

Automatically doing the jobs I used to manually do!

## EC2 Startup

This will ensure the jobs are completed correctly, runs in the following order:
- System Startup
- Update scraper
- Start scraper

```crontab
@reboot ./SystemStartup.sh && ./UpdateScraper.sh && ./StartScraper.sh
```

## Midnight

This will reboot everything so we can check for updates:
- Stop scraper
- Update scraper
- Start scraper

```crontab
00 00 * * * ./StopScraper.sh && ./UpdateScraper.sh && ./StartScraper.sh
```

# Individual Scripts

## System Startup

Ensure everything is running when EC2 Starts

```bash
service docker start
docker container prune
docker run --rm -d -p 9090:9090 --name prometheus -v ~/prometheus:/etc/prometheus prom/prometheus --config.file=/etc/prometheus/prometheus.yml --web.enable-lifecycle
./node_exporter-*.*-amd64/node_exporter
```

## Start scraper

Correctly startup thescraper

```bash
docker run --rm -d -p 4444:4444 -p 7900:7900 --shm-size="2g" selenium/standalone-firefox
docker run --rm -d sk1y101/exoplanet-scraping --address localhost:4444 --upload
```

## Update scraper

Update everything needed for the scraper

```bash
docker pull sk1y101/exoplanet-scraping
docker pull selenium/standalone-firefox
```

## Stop scraper

Executed at midnight each day to safely shutdown things

```bash
docker stop sk1y101/exoplanet-scraping
docker stop selenium/standalone-firefox
```

## On creation

To enable these scripts for execution, the command `sudo chmod +x <file>.sh` is required.