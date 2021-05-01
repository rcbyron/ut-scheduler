# UT Scheduler
A responsive web app for generating optimal class schedules based on class times, GPA, and professor reviews by scraping course data from numerous websites

## Dependencies
- Python 2 / 3
- Falcon
- PyMySQL
- ScraPy

## Sections
This project is comprised in 3 parts:
- api - for serving the MySQL cached data via RESTful calls
- website - for frontend HTML/CSS
- worker - for periodically scraping and saving course data
