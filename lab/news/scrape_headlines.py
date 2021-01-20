import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import sys
import json
import os

def blacklist(link):
    blacklist = ['www.nasdaq.com']
    skip = False
    for b in blacklist:
        if b in link:
            skip = True

    return skip

def scrape_news(query="best+stocks+to+buy+this+week"):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}    
    stocklinks = []

    try:
        url = 'https://www.bing.com/news/search?q={}'.format(query)
        results = requests.get(url, headers=headers)
    except:
        print("Unexpected error:", sys.exc_info()[0])

    soup = BeautifulSoup(results.text, 'html.parser')
    links = soup.find_all("a", {"class": "title"})

    for link in links[:10]:
        if (blacklist(link['href'])):
            continue

        print(link['href'])

        page = requests.get(link['href'], headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        all_links = soup.find_all("a")

        # print(len(all_links))
        for l in all_links:
            if ('NASDAQ:' in l.text):
                stocklinks.append(l)
            if ('NYSE:' in l.text):
                stocklinks.append(l)

        time.sleep(0.5)

    for stock in stocklinks:
        print(stock.text)
