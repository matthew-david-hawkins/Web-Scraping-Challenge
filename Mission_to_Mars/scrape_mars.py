# Import dependencies
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time
import re
import pandas as pd

# Define a function the visits a webpage and returns a beautful soup
def get_soup(url):
    
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)
    
    # Visit with selenium
    browser.visit(url)

    # Wait 1 second to allow the page to load
    time.sleep(3)

    # Save the browser's html as text
    html = browser.html

    # Convert html text to beautiful soup object
    soup = bs(html, 'html.parser')

    # Print the webpage title
    print(soup.title.text +'\n')
    
    return soup

# Function that scrapes News Title and Summary from the Nasa Mars News site and returns a list of dictionaries
def get_news(base_url, args):
    
    url = base_url + args
    
    # Get soup
    soup = get_soup(url)

    # Identify the Title and Summary via div.content_title and div.article_teaser_body
    results = soup.find_all('div', class_="list_text")

    # news is a list of dictionaries
    news = []
    # Iterate over the results 
    for result in results:

        # Only Retrieve results if they have a summary text
        try:
            date = result.find('div', class_="list_date").text
            summary = result.find('div', class_="article_teaser_body").text
            headline = result.find('div', class_="content_title").get_text()
            #print(f"{date} : {headline}\n{summary}\n\n")

            # Save results to a dictionary
            dictionary = {}
            dictionary= {
                'date' : date,
                'headline' : headline,
                'summary' : summary
            }

            # Append list with dictionary
            news.append(dictionary)

        # If the article is missing content, skip it
        except:
            print("Nothing found")

    return news

# Function which scrapes the JPL 'Featured Image' and returns the url to the image
def get_featured_img(base_url, args):
    
    url = base_url + args
    
    soup = get_soup(url)

    # Identify the featured image url via section.centered_text clearfix main_feature primary_media_feature single
    result = soup.find_all('section', class_="centered_text clearfix main_feature primary_media_feature single")[0]

    # Split the string with '(' or ')'
    string = re.split('[(|)]', result.article['style'])[1]

    # Strip the single quotes
    string = string[1:-1]

    # Combine with base url
    image_url = base_url + string

    return image_url

# A function which scrapes Mars weather data from the Mars Weather Twitter Page and returns the latest weather
def get_weather(base_url, args):
    
    url = base_url + args
    
    soup = get_soup(url)

    # Identify the weather report via tweet -> tweet-text
    results = soup.find_all('div', class_="tweet")

    # The latest tweet is in the first result; save in a variable
    mars_weather = results[0].find('p', class_="tweet-text").text

    # Remove the link off the end
    mars_weather = mars_weather.split('pic.twitter')[0]

    # The first result contains the latest tweet.
    print('Latest weather report:''\n\n' + mars_weather + '\n\n')

    ## Print all tweets for good measure
    #for result in results:
    #    print(result.find('p', class_="tweet-text").get_text())
    
    return mars_weather

# Function which scapes Mars facts from space-facts.com/mars and returns a dataframe
def get_facts(base_url, args):
    
    url = base_url + args
    
    # Scrape for data tables with pandas
    tables = pd.read_html(url)

    fact_table = tables[0].to_html()
    
    # The relevant table is the first table
    return fact_table

# Function which scrapes images of the Mars Hemispheres and returns a list of dicntionaries of titles and urls
def get_hemis(base_url, args):
    
    url = base_url + args

    # Get soup of the main page
    soup = get_soup(url)

    # Find urls to high-res images via section -> results-accordian -> div.item, a.href.text 
    results = soup.find_all('section', {'id':'results-accordian'})[0].find_all('div', class_='item')
    inter_urls = []

    # Iterate over each link to the sub-page
    for result in results:
        try:
            # Find urls via ->a.hef
            inter_urls.append(base_url+result.a['href'])
        except:
            print("null")

    # 
    hemi_list = []
    for url in inter_urls:
        # Visit each link
        soup = get_soup(url)
        try:
            img_url = soup.find_all('div', class_='downloads')[0].find_all('li')[0].a['href']
            img_title = soup.title.text
            img_title = img_title.split(" |")[0]
            dictionary = {
                'title' : img_title,
                'img_url' : img_url
            }
            hemi_list.append(dictionary)
        except:
            print("null")

    return hemi_list

def scrape():
    # Get news about Mars
    url = 'https://mars.nasa.gov/news/'
    args = ''
    news = get_news(url,'')
    #print(news)

    # Get featured image
    base_url = 'https://www.jpl.nasa.gov'
    args = '/spaceimages/?search=&category=Mars'
    image_url = get_featured_img(base_url, args)

    # Get weather information
    url = 'https://twitter.com/marswxreport?lang=en'
    args = ''
    mars_weather = get_weather(url, args)

    # Get Mars facts
    url = 'https://space-facts.com/mars'
    args = ''
    fact_table = get_facts(url,args)

    # Get images of hemispheres
    base_url = 'https://astrogeology.usgs.gov/'
    args = 'search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemi_list = get_hemis(base_url, args)

    # Save scraping results to a dictionary
    scrape_dictionary = {
        'news' : news[0],
        'featured_image' : image_url,
        'mars_weather' : mars_weather,
        'mars_facts' : fact_table,
        'hemispheres' : hemi_list
    }

    return scrape_dictionary