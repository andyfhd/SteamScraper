# SteamScraper

## Get Started
* script configs are at the top
* update working_directory to your own location and place chromedriver.exe into the same directory
* install missing packages (e.g. selenium)
* run the script (in Spyder: select all code and F9 or command line: python steam_scraper.py)

## Configuration
* urls: list of game pages (note: some games have different page structure, e.g. Witcher 3 Game of the Year Edition, new games may not have a review section, e.g. Shadow of the Tomb Raider)
* delay: main page load wait time in seconds (7s work for all example games, 5s occasionally causes timeout exception)
* review_delay: wait time between each scroll in the review section
* review_scrolls: number of scrolls for review section

## Change Log
### v2
* add Selenium (page navigation and scrolling)
* write output into JSON and two CSVs
* restructure into a single script
