from selenium import webdriver
from time import sleep
import os
import random
from parsel import Selector
from datetime import date
import json


##################
# LINKEDIN LOGIN #
##################
def login(driver):
    """Initialize a selenium webdriver and login

    Parameters
    ----------
    driver      :   selenium.webdriver.chrome.webdriver.WebDriver object
    """


    # Go to the LinkedIn website
    driver.get("https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin")

    # Find and supply the username
    username = driver.find_element_by_name("session_key")
    username.send_keys(os.environ['LI_USERNAME']) 
    sleep(random.uniform(.5, 3))

    # Find and supply the password
    password = driver.find_element_by_name("session_password")
    password.send_keys(os.environ['LI_PASSWORD'])
    sleep(random.uniform(.05, .3))

    # Find and click the log in button
    log_in_button = driver.find_element_by_xpath('//*[@id="app__container"]/main/div/form/div[3]/button')
    log_in_button.click()
    sleep(random.uniform(.1, .5))


def scrape_connections(driver, profile_url, depth=0, base_data=None):
    """
    Parameters
    ----------
    driver      :   selenium.webdriver.chrome.webdriver.WebDriver object
    profile_url :   str
        The url for the starting profile that you want to scrape
    depth       :   int
        How many connections away from the startin profile you want to scrape. Either 0 or 1.
    base_data   :   dict
        Starting data for your connections
    """

    driver.get(profile_url)
    data = dict()

    # Navigate to the connections page
    connections_page_base = driver.find_element_by_css_selector('[data-control-name="topcard_view_all_connections"]').get_attribute('href')  
    driver.get(connections_page_base)
    sleep(random.uniform(.1, .5))

    # Scroll to the bottom to load the entire page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(random.uniform(.3, 1))
    total_pages = int(driver.find_elements_by_css_selector('li[class*=artdeco-pagination]')[-1].text)
    
    
    base_name = url_to_name(profile_url)
    data.update(scrape_page(driver, base_name))
    # Scrape only the base coneection's pages
    for page_num in range(2, total_pages+1):
        data.update(scrape_page(driver, base_name))
        # Go to the next page
        next_page = connections_page_base + '&page={}'.format(page_num)
        driver.get(next_page)
        sleep(random.uniform(.1,.5))
        # Scroll to the bottom to load the entire page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(random.uniform(.3,1))

    return data



def scrape_page(driver, connector):
    """Given a selenium webdriver object for a LinkedIn connections page this function
    pulls the page source and yanks connection details and stores them in variables. Each
    variable should be a list of length 10.

    Parameters
    ----------
    driver      :   selenium.webdriver.chrome.webdriver.WebDriver object
    connector   :   str
        The base connector that is being scraped
    Returns
    -------
    dict
    """
    sel = Selector(text=driver.page_source) 

    # These are lists, all should be length 10
    # MAKE MORE ROBUST? CHECK LENGTHS?
    names = sel.css('span[class*=actor-name]::text').getall()
    distances = sel.css('span[class*=dist-value]::text').getall()
    headlines = sel.css('span[dir*=ltr]::text').getall()[::2]
    locations = sel.css('span[dir*=ltr]::text').getall()[1::2]
    connection_urls = sel.css('a[class*=search-result__result-link]::attr(href)').getall()[::2]
    connection_urls = ['https://www.linkedin.com/' + url for url in connection_urls]

    data = dict()
    data['connections'] = list()

    for n in range(len(names)):
        data['connections'].append({
            'name'      :   names[n],
            'distance'  :   distances[n],
            'headline'  :   headlines[n],
            'location'  :   locations[n],
            'url'       :   connection_urls[n],
            'id'        :   url_to_name(connection_urls[n]),
            'connector' :   connector,
        })
    
    return data


def url_to_name(url):
    """Take a LinkedIn profile url and return the name id

    Parameters
    ----------
    url :   str
        LinkedIn profile url
    """

    return url.strip('/').split('/')[-1] 


def save_connections(connection_dict, url):
    """Given a nested dictionary of connections and a LinkedIn profile url save a json file of the connections.

    Parameters
    ----------
    connection_dict :   dict
        A dictionary of connections
    url             :   str 
        The url of the current profile
    """
    
    today = date.today().strftime('%y%m%d')
    path = './data' + '_' + today + '/'
    if not os.path.exists(path):
        os.makedirs(path)

    fname = path + today + '_' + url_to_name(url) + '.json'
    with open(fname, 'w') as f:
        json.dump(connection_dict, f)