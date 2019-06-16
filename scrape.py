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

# If I wanted to go full bore and gather connections of connections
"""
# Scrape connections of connections
for connection in base_connections['connections']:
    data = u.scrape_connections(driver, connection['url'])
    u.save_connections(data, connection['url'])
"""