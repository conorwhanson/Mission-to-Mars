
# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import numpy as np
import requests

# set path
exec_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **exec_path, headless=False)

# ## Mars News
##########################
# visit the mars NASA site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# convert browser html to soup object
html = browser.html
red_soup = soup(html, 'html.parser')

slide_elem = red_soup.select_one('div.list_text')

# find Mars news title
news_title1 = slide_elem.find('div', class_='content_title').get_text()
news_title1

# find Mars news summary
summary = slide_elem.find('div', class_='article_teaser_body').get_text()
summary

# ## Image
###########################
# Scrape the featured image
 
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# find the button for featured image and click it
full_feature_img = browser.find_by_tag('button')[1]
full_feature_img.click()

# set up html parser
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# url above is only partial; need to add it onto the base url and save it as a variable
img_url = f"https://spaceimages-mars.com/{img_url_rel}"
img_url

# ## Mars Facts
############################
# read in facts about Mars with pd.read_html
df = pd.read_html('https://galaxyfacts-mars.com/')[0]
df.columns = ('description','Mars','Earth')
df.set_index('description', inplace=True)
df

# turn the pulled table back into HTML for coding
df.to_html()
