from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

def scrape():
    mars_dict = {}
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

    # ### NASA Mars News

    print('Gathering Mars News')
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(4)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find('div','content_title').text.strip()
    news_p = soup.find('div',class_='article_teaser_body').text.strip()
    mars_dict["news_title"] = news_title
    mars_dict["news_p"] = news_p
    print('Done')

    # ### JPL Mars Space Images

    print('Gathering Mars Images')
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('div',class_='carousel_items').find('article').find('footer').find('a')['data-fancybox-href']
    base_url = 'https://www.jpl.nasa.gov'
    featured_img = base_url + img
    mars_dict["featured_img"] = featured_img
    print('Done')

    # ### Mars Weather

    print('Gathering Mars Weather')
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    tweet = soup.find_all('div',class_ = "content")
    for i in range(len(tweet)-1):
        if tweet[i].find('a')["data-user-id"] == '786939553':
            mars_weather = tweet[i].find(class_='js-tweet-text-container').text.strip()
            break
    mars_dict["mars_weather"] = mars_weather
    print('Done')

    # ### Mars Facts

    print('Gathering Mars Facts')
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['Field','Value']
    df.set_index('Field', inplace=True)
    df.to_html('table.html')
    mars_dict["mars_facts"] = df.to_html()
    print('Done')

    # ### Mars Hemispheres 

    print('Gathering Mars Hemispheres')
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    Hemispheres = ['Cerberus Hemisphere',
                'Schiaparelli Hemisphere',
                'Syrtis Major Hemisphere',
                'Valles Marineris Hemisphere'
                ]
    base_url = 'https://astrogeology.usgs.gov'
    hemisphere_image_urls = []
    for i in range(len(Hemispheres)):
        hemisphere_dict = {}
        browser.click_link_by_partial_text(Hemispheres[i]+' Enhanced')
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img = soup.find('img',class_='wide-image')['src']
        full_url = base_url + img
        browser.click_link_by_partial_text('Back')
        time.sleep(2)
        hemisphere_dict = {
            'title': Hemispheres[i],
            'img_url': full_url
        }
        hemisphere_image_urls.append(hemisphere_dict)
    mars_dict["hemisphere_image_urls"] = hemisphere_image_urls
    print('Done')

    return mars_dict

if __name__ == "__main__":
    scrape()
