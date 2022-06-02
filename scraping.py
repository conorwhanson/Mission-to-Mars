
# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import numpy as np
import requests
import datetime as dt
import time


def scrape_all():
    # set path
    exec_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **exec_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    hemispheres = hemi_data(browser)

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_img": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemispheres

    }
    browser.quit()
    return data

def mars_news(browser):
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

    try:
        slide_elem = red_soup.select_one('div.list_text')

        # find Mars news title
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # find Mars news summary
        summary = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, summary

def featured_image(browser):
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

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    # url above is only partial; need to add it onto the base url and save it as a variable
    img_url = f"https://spaceimages-mars.com/{img_url_rel}"

    return img_url

def mars_facts():
    # ## Mars Facts
    ############################
    try:
        # read in facts about Mars with pd.read_html
        df = pd.read_html('https://galaxyfacts-mars.com/')[0]

    except BaseException:
        return None

    df.columns = ('Description','Mars','Earth')
    df.set_index('Description', inplace=True)

    # turn the pulled table back into HTML for coding
    return df.to_html()

def hemi_data(browser):

    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    hemi_soup = soup(html, 'html.parser')
    hemi = hemi_soup.find('div', {'class':'results'}).find_all('div', {'class','item'})

    hemispheres = []

    for item in hemi:
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

        hemispheres.append(data)
        
    return hemispheres

if __name__ == "__main__":
    # if it's running as a script, then print the scraped data
    print(scrape_all())