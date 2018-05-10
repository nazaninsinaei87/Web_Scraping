from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()
    scraped_data = {}
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')

    news_title = soup.find('div', class_="content_title").text
    news_paragraph = soup.find('div', class_="rollover_description_inner").text

    scraped_data["news_title"] = news_title
    scraped_data["news_paragraph"] = news_paragraph

    # # JPL Mars Space Images - Featured Image
    
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    
    html = browser.html
    soup = bs(html, 'html.parser')

    image_url = soup.body.footer.a["data-fancybox-href"]
    featured_image_url = 'https://www.jpl.nasa.gov'+ image_url
    
    scraped_data ["featured_image_url"] = featured_image_url
    
    # # Mars Weather
    
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    
    html = browser.html
    soup = bs(html, 'html.parser')
    
    mars_weather = soup.body.find('div', class_='js-tweet-text-container').p.text
    
    scraped_data["mars_weather"] = mars_weather
    # # Mars Facts
    
    url = 'https://space-facts.com/mars/'
    table = pd.read_html(url)
    
    df = table[0]
    df.columns = ["Facts","Values"]
    df.set_index("Facts", inplace=True)
    
    html_table = df.to_html()
    html_table.replace("\n","")
    
    # # Mars Hemisperes
    
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html,'html.parser')
    
    results = soup.find_all('h3')
    h3=[]
    for result in results:
        h3.append(result.text)
    print(h3)
    
    
    hemisphere_image_urls = []
    for text in h3:
        browser.find_by_text(text).click()
        html = browser.html
        soup = bs(html, 'html.parser')
        title_text = soup.body.find('h2', class_='title').text
        image_url = soup.body.find('div', class_='downloads').find('li').a['href']
        browser.click_link_by_partial_text('Back')
        hemisphere_image_urls.append (
                {"title": title_text,
                  "img_url": image_url})

    
    scraped_data["hemisphere_image_urls"] = hemisphere_image_urls
    
    return scraped_data


