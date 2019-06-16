import utilities as u
from selenium import webdriver
import json
import os


# Initialize the webdriver
driver = webdriver.Chrome(os.environ['CHROME_DRIVER'])

# Log in to LinkedIn
u.login(driver)

# Go to your profile page
profile_url = driver.find_element_by_css_selector('[data-control-name="identity_profile_photo"]').get_attribute('href')

# Scrape connections from your profile
base_connections = u.scrape_connections(driver, profile_url)
u.save_connections(base_connections, profile_url)

# Scrape connections of connections
for connection in base_connections['connections']:
    data = u.scrape_connections(driver, connection['url'])
    u.save_connections(data, connection['url'])





"""
driver.get(profile_url)

# Now to the connections page
connections_page_base = driver.find_element_by_css_selector('[data-control-name="topcard_view_all_connections"]').get_attribute('href')  
driver.get(connections_page_base)
u.sleep(u.random.uniform(.1, .5))

# Scroll to the bottom to load the entire page
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
u.sleep(u.random.uniform(.3, 1))
total_pages = int(driver.find_elements_by_css_selector('li[class*=artdeco-pagination]')[-1].text)

# Scrape the pages
data = dict()
for page_num in range(2, total_pages+1):
    data.update(u.scrape())
"""