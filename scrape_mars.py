from splinter import Browser
import pandas as pd
import lxml.html as lh
from bs4 import BeautifulSoup as bs
import time
import requests

# Initialize browser
def init_browser(): 
    exec_path = {'executable_path': '/app/.chromedriver/bin/chromedriver'}
    return Browser('chrome', headless=True, **exec_path)

# Create global dictionary to be imported into Mongo
mars_info = {}

# A. NASA MARS NEWS
def scrape_mars_news():
    try: 

        browser = init_browser()

        # Use Splinter Module to Visit Nasa news url
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        html = browser.html

        # Use Beautiful Soup to parse html
        soup = bs(html, 'html.parser')

        # news title = x, News Paragraph = y
        news_title = soup.select_one('ul.item_list li.slide')
        x = news_title.find("div", class_='content_title').getText()
        y = news_title.find("div", class_='article_teaser_body').getText()

        # Dictionary entry from MARS NEWS
        mars_info['news_title'] = x
        mars_info['news_paragraph'] = y

        return mars_info

    finally:

        browser.quit()

# B. FEATURED IMAGE
def scrape_mars_image():

    try: 
        browser = init_browser()
        wait_time = 1
        #browser.is_element_present_by_css("img.jpg", wait_time=1)

        # Visit Mars Space Images through splinter module
        featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(feat_image)# Visit Mars Space Images through splinter module

        html_image = browser.html

        # Use Beautiful Soup to parse html
        soup = bs(html_image, 'html.parser')

        # get image 
        feat_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

        # Website Url 
        main_url = 'https://www.jpl.nasa.gov'

        # Concatenate website url with scrapped route
        feat_image_url = main_url + feat_image_url

        # Display full link to featured image
        feat_image_url 

        # Dictionary entry from FEATURED IMAGE
        mars_info['feat_image_url'] = feat_image_url 
        
        return mars_info
    finally:

        browser.quit()


# C. Mars Facts
def scrape_mars_facts():

    # Visit Mars facts url 
    facts_url = 'http://space-facts.com/mars/'

    # Use Pandas  read to parse url
    mars_facts = pd.read_html(facts_url)

    # Create mars_df from mars_facts
    mars_df = mars_facts[0]

    # Assign columns 
    mars_df.columns = ['Description','Value']

    # Set the index to Description column
    mars_df.set_index('Description', inplace=True)

    # Save html code to assets folde
    data = mars_df.to_html()

    
    mars_info['mars_facts'] = data

    return mars_info


# D. MARS HEMISPHERES

def scrape_mars_hemispheres():

    try: 
        browser = init_browser()

        # Use splinter to go to the  hemispheres website 
        hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemi_url)

        html_hemi = browser.html

        # Use Beautiful Soup to parse HTML
        soup = bs(html_hemispheres, 'html.parser')

        # Get info on mars hemi facts
        items = soup.find_all('div', class_='item')

        # Create empty list for hemisphere urls 
        hemi_image_urls = []

        # Store the main ul 
        hemis_main_url = 'https://astrogeology.usgs.gov' 

        # Create loop for items stored
        for i in items: 
            # Store title
            title = i.find('h3').text
            
            # Store link that leads to full image website
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
            # Visit the link that contains the full image website 
            browser.visit(hemi_main_url + partial_img_url)
            
            # HTML Object of individual hemisphere information website 
            partial_img_html = browser.html
            
            # Use Beautiful Soup to parse all individual hemisphere information website 
            soup = bs( partial_img_html, 'html.parser')
            
            # get image source 
            img_url = hemi_main_url + soup.find('img', class_='wide-image')['src']
            
            # Append info into a list of dictionaries 
            hemi_image_urls.append({"title" : title, "img_url" : img_url})

        mars_info['hemisphere_image_urls'] = hemi_image_urls

        
        # Return mars_data dictionary 

        return mars_info
    finally:

        browser.quit()