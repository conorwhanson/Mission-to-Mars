
# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

# ### JPL Space Images Featured Image
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'

# ### Mars Facts

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()

df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)

# Save as variable to write to Mongo
df.to_html()

# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)

html = browser.html
hem_soup = soup(html, 'html.parser')

items = hem_soup.find('div', {'class':'results'}).find_all('div', {'class','item'})
len(items)

test = items[0]
link = test.find('a', {'class':'itemLink'})['href']

full_url = url+link

browser.visit(full_url)

html = browser.html
img_soup = soup(html, 'html.parser')

img_link = img_soup.find('img', {'class': 'wide-image'})['src']

img_url = url+img_link

img_soup.find('h2', {'class':'title'}).text.split("Enhanced")[0].strip()

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for item in items:
    link = item.find('a', {'class':'itemLink'})['href']
    full_url = url+link
    browser.visit(full_url)
    
    time.sleep(1)
    html = browser.html
    hem_img_soup = soup(html, 'html.parser')
    
    img = hem_img_soup.find('img', {'class': 'wide-image'})['src']
    big_img = url+img
    
    title = hem_img_soup.find('h2',{'class':'title'}).text.split("Enhanced")[0].strip()
    
    data = {'img_url': big_img, 'title': title}
    
    hemisphere_image_urls.append(data)

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()
