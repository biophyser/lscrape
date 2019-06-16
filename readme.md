# Lscrape

I put together an automated browser for LinkedIn using selenium. Currently, my focus is to investigate my 1st and 2nd order connections for educational purposes.

**Future Plans:**

If I want to scrape quickly I'll probably use `scrapy` instead. At this point I like watching it go.

## Getting Started

If you also want to use this script download it and the Chrome webdriver described below. Then set some envrionment variables and you're off and running.

### Prerequisites

**Python packages:**
- `parsel`
- `selenium`

Use pip or conda to install any or all of these:

`pip install parsel selenium gspread oauth2client`

or

`conda install parsel selenium gspread oauth2client`

**Other things:**
- Google Chrome webdriver
  - Get it [here](http://chromedriver.chromium.org/downloads)
- Environment Variables
  - I set environment variables for a specific `conda` environment by following [these instructions](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#macos-and-linux)
  - I did this for both my LinkedIn Login Credentials and the Chrome webdriver location

### Installing

Currently this is a one-off script. To use download it and run it like this:

`python scrape.py`

Hopefully, I'll package it up nicer in the future :)

## Authors

* **Jeremy Anderson** - [Biophyser](https://github.com/biophyser)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* I learned some basics about `selenium` [here](https://www.linkedin.com/pulse/how-easy-scraping-data-from-linkedin-profiles-david-craven/)
* [This blog post](http://tatiyants.com/how-to-use-html5-data-attributes-with-jquery-and-selenium/) helped me figure out how to identify a data attribute name as an argument to `selenium`'s `find_element_by_css_selector` function.