import django
from django.apps import apps
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
from .functions import *
from ..core.api.batch import batchQuote
from ..core.functions import dataSanityCheck, frequencyInList, chunks
from ..core.output import printStockResults
from ..fintwit.tweet import send_tweet
import colored
from colored import stylize
import time
import sys
import json
import os
django.setup()


def exchanges():
    return [
        'NYSE',
        'NASDAQ',
        'LSE',
        'TSX',
        'NSE',
        'ASX',
        'BSE',
        'TYO',
        'SSE',
        'OTC',
        'OTCMKTS'
    ]


def scanHeap(heap):
    """
    This function takes a list of text blobs and scans all words for potential stocks based on a regex formula. 
    The function will cross-reference every potential stock with IEX to determine whether or not it is an actual stock.
    Strings that do not pass the test will be sent to the blacklist to prevent future lookups.

    Parameters
    ----------
    heap     : list
               list of text blobs taken from reddit

    Returns
    -------
    dict
        list of results confirmed to be stocks
    """
    target_strings = []
    sentiment_index = {}
    for h in heap:
        # TODO: Make news scraper use this reddit scraping formula.

        # Find all capital letter strings, ranging from 1 to 5 characters, with optional dollar
        # signs preceded and followed by space.
        tickers = re.findall(r'[\S][$]?[A-Z]{1,5}[\S]*', str(h))

        for tick in tickers:
            tformat = removeBadCharacters(tick)
            target_strings.append(tformat)

    blacklist = blacklistWords()
    possible = []

    for string in target_strings:
        if (string):
            if ((not string) or (string in blacklist)):
                continue

            possible.append(string)

    results = []
    stockfound = []

    unique_possibles = list(dict.fromkeys(possible))
    chunked_strings = chunks(unique_possibles, 100)

    apiOnly = [
        'symbol',
        'companyName',
        'close',
        'changePercent',
        'ytdChange',
        'volume'
    ]

    print(stylize("{} possibilities".format(len(unique_possibles)), colored.fg("yellow")))

    for i, chunk in enumerate(chunked_strings):

        print(stylize("Sending heap to API", colored.fg("yellow")))
        batch = batchQuote(chunk)
        time.sleep(1)

        for ticker, stockinfo in batch.items():

            if (stockinfo.get('quote', False)):
                result = {}
                stockfound.append(ticker)
                freq = frequencyInList(possible, ticker)            

                print(stylize("{} stock found".format(ticker), colored.fg("green")))
                if (freq > 1):
                    result = {
                        'ticker': ticker,
                        'frequency': freq,
                    }
                    filteredinfo = {key: stockinfo['quote'][key] for key in apiOnly}
                    result.update(filteredinfo)
                    results.append(result)

    # Updating blacklist
    for un in unique_possibles:
        if (un not in stockfound):
            blacklist.append(un)

    updateBlacklist(blacklist)
    return results


def scrape_news(query):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    tickers = []
    heap = []

    try:
        url = 'https://www.bing.com/news/search?q={}'.format(query)
        results = requests.get(url, headers=headers)
    except:
        print(stylize("Unexpected error:", colored.fg("red")))
        print(stylize(sys.exc_info()[0], colored.fg("red")))

    soup = BeautifulSoup(results.text, 'html.parser')
    links = soup.find_all("a", {"class": "title"})

    for link in links:
        if (link in blacklistUrls()):
            continue

        print(stylize("Searching... "+link['href'], colored.fg("yellow")))

        page = requests.get(link['href'], headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        heap.append(soup.text)
        time.sleep(1)

    results = scanHeap(heap)    


    #     all_links = soup.find_all("a", href=True)

    #     for l in all_links:
    #         for exc in exchanges():
    #             searchstr = exc+':'
    #             if (searchstr in l.text):
    #                 tickers.append(l.text.split(':')[1])
    #             if ((l.get('href', False)) and ('quote' in l['href'])):
    #                 tickers.append(l.text)

    #     time.sleep(1)

    # if (tickers):
    #     tickers = clean_tickers(tickers)
    #     printStockResults(tickers)