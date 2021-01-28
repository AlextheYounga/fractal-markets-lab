import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
from ..core.api import quoteStatsBatchRequest
from ..core.functions import dataSanityCheck
from ..core.output import printTable, printFullTable, writeCSV
from ..fintwit.tweet import send_tweet
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


def print_results(tickers):
    print("\n")
    results = []
    batch = quoteStatsBatchRequest(tickers)

    for ticker, stockinfo in batch.items():

        if (stockinfo.get('quote', False) and stockinfo.get('stats', False)):
            quote = stockinfo.get('quote')
            stats = stockinfo.get('stats')
            price = quote.get('latestPrice', 0)

            ttmEPS = stats.get('ttmEPS', None)
            day5ChangePercent = round(dataSanityCheck(stats, 'day5ChangePercent') * 100, 2)
            month1ChangePercent = round(dataSanityCheck(stats, 'month1ChangePercent') * 100, 2)
            ytdChangePercent = round(dataSanityCheck(stats, 'ytdChangePercent') * 100, 2)
            volume = dataSanityCheck(quote, 'volume')
            previousVolume = dataSanityCheck(quote, 'previousVolume')
            changeToday = round(dataSanityCheck(quote, 'changePercent') * 100, 2)

            # Critical
            week52high = dataSanityCheck(stats, 'week52high')

            critical = [week52high, volume, previousVolume]

            if ((0 in critical)):
                continue

            fromHigh = round((price / week52high) * 100, 3)
            volumeChangeDay = (float(volume) - float(previousVolume)) / float(previousVolume) * 100

            keyStats = {
                'ticker': ticker,
                'name': stats['companyName'],
                'lastPrice': price,
                'peRatio': stats.get('peRatio', None),
                'week52': week52high,
                'changeToday': changeToday,
                'day5ChangePercent': day5ChangePercent if day5ChangePercent else None,
                'month1ChangePercent': month1ChangePercent if month1ChangePercent else None,
                'ytdChangePercent': ytdChangePercent if ytdChangePercent else None,
                'volumeChangeDay':  "{}%".format(round(volumeChangeDay, 2)),                
                'fromHigh': fromHigh,
                'ttmEPS': ttmEPS
            }

            results.append(keyStats)

    if results:
        today = date.today().strftime('%m-%d')
        writeCSV(results, 'lab/news/output/appeared_in_news_{}.csv'.format(today))

        printFullTable(results, struct='dictlist')

        # Tweet
        # tweet = ""
        # for i, data in enumerate(results):
        #     ticker = '${}'.format(data['ticker'])
        #     changeToday = data['changeToday']
        #     tweet_data = "{} +{}% \n".format(ticker, changeToday)
        #     tweet = tweet + tweet_data

        # send_tweet(tweet, True)


def scrape_news(query="best+stocks+to+buy+this+week"):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    tickers = []

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

        print("Searching... "+link['href'])

        page = requests.get(link['href'], headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        all_links = soup.find_all("a")

        for l in all_links:
            if ('NASDAQ:' in l.text):
                tickers.append(l.text.split(':')[1])
            if ('NYSE:' in l.text):
                tickers.append(l.text.split(':')[1])

        time.sleep(1)

    print_results(tickers)
