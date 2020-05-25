#!/usr/bin/env python
import pandas as pd
import requests as req
from bs4 import BeautifulSoup
from selenium import webdriver
from splinter import Browser
import requests
import time


# INITIALIZE CHROMEDRIVER AS BROWSWER
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # ### VISIT MARS.NASA.GOV FOR MARS NEWS
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(5)

    #PARSE HMTL FROM BROWSER AND FIND THE NEWS
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    all_news = soup.find_all('div', class_='list_text',limit=1)
    latest_news = all_news[0]
    latest_title = latest_news.find('div', class_='content_title').text
    latest_para = latest_news.find('div', class_='article_teaser_body').text
    print(f"Title: {latest_title}\nBody: {latest_para}")

    #Find image of Mars
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Use the image ID to click link to full_image
    browser.click_link_by_id('full_image')

    # Use partial href to click for full image page
    browser.click_link_by_partial_href('spaceimages/details.php')

    #Scrape the full html from the page
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find the link to the main_image class for the .jpg file
    main_image = soup.find('img', class_='main_image')
    main_image['src']

    #Get the full URL for the main image
    main_image = f"https://www.jpl.nasa.gov/{main_image['src']}"
    print(f"Image of mars: {main_image}")

    # ### Find the weather on Mars with Twitter

    url = 'https://twitter.com/marswxreport?lang=en'
    data = requests.get(url)
    html = BeautifulSoup(data.text, 'html.parser')
    tweets = html.select('#timeline li.stream-item')

    for tweet in tweets:
        tweet_id = tweet['data-item-id']
        tweet_text = tweet.select('p.tweet-text')[0].get_text()

    print(f"Tweet Text: {tweet_text}")

    #Get Mars Facts into dataframe
    url = 'https://space-facts.com/mars/'
    response = requests.get(url)
    mars_facts_df = pd.read_html(response.text)
    mars_facts = mars_facts_df[0].to_dict()
    mars_facts = {mars_facts[0][0]: mars_facts[1][0],
                mars_facts[0][1]: mars_facts[1][1],
                mars_facts[0][2]: mars_facts[1][2],
                mars_facts[0][3]: mars_facts[1][3],
                mars_facts[0][4]: mars_facts[1][4],
                mars_facts[0][5]: mars_facts[1][5],
                mars_facts[0][6]: mars_facts[1][6],
                mars_facts[0][7]: mars_facts[1][7],
                mars_facts[0][8]: mars_facts[1][8]
                }

    #Get Mars Hemispheres
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(url)
    time.sleep(1)
    soup = BeautifulSoup(response.text, 'html.parser')

    #Elements 4-7 contain the 4 URLs I want to visit
    links = soup.find_all('a',href=True)
    links_index = [4,5,6,7]

    photo_links = []
    for link in links_index:
        try:
            url = f"https://astrogeology.usgs.gov{links[link]['href']}"
            response = requests.get(url)
            print(url)
            name = url.split("/")[7]
            name = name.split("_")[0]
            print(name)
            print(response)
            time.sleep(1)
            soup = BeautifulSoup(response.text,"html.parser")
            downloads = soup.find('div',class_="downloads")
            original = downloads.find_all('li')[1]
            original = original.find('a')['href']
            photo_links.append({"title": f"{name} hemisphere", "img_url": original})
        except:
            print("error: could not find link")

    print(photo_links)

    mars_info = {
        "News title": latest_title,
        "News Paragraph": latest_para,
        "Mars Image": main_image,
        "Weather": tweet_text,
        "Mars facts": mars_facts,
        "hemispheres": photo_links
    }
    return mars_info