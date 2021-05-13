import praw
from praw.models import MoreComments
import colored
from colored import stylize
from ..core.functions import frequencyInList, chunks
from ..core.output import printFullTable
from ..core.api.batch import batchQuote
from .functions import *
import time
import datetime
import re
import sys
import json
import os
import pprint
from ..fintwit.tweet import send_tweet, translate_data
from dotenv import load_dotenv
load_dotenv()


def scrapeWSB(sendtweet=False):
    reddit = praw.Reddit(
        client_id=os.environ.get("REDDIT_CLIENT"),
        client_secret=os.environ.get("REDDIT_SECRET"),
        user_agent="Hazlitt Data by u/{}".format(os.environ.get("REDDIT_USERNAME")),
        username=os.environ.get("REDDIT_USERNAME"),
        password=os.environ.get("REDDIT_PASSWORD"),
    )

    subreddit = reddit.subreddit("wallstreetbets")

    urls = []
    heap = []

    for submission in subreddit.hot(limit=20):
        post_time = datetime.datetime.fromtimestamp(submission.created)
        print(stylize("r/wallstreetbets postdate={}: ".format(str(post_time)) + submission.title, colored.fg("green")))
        urls.append(submission.url)
        heap.append(submission.title)

        for top_level_comment in submission.comments:
            if isinstance(top_level_comment, MoreComments):
                continue
            heap.append(top_level_comment.body)

    # print(json.dumps(heap, indent=1))


    target_strings = []
    for h in heap:
        # Find all strings with $ dollar signs
        target_strings.append(re.findall(r'[$][A-Za-z][\S]*', str(h)))
        # Find all capital letter strings, ranging from 1 to 5 characters, preceded and followed by space.
        capitals = re.findall(r'[\S][A-Z]{1,5}[\S]*', str(h))
        for cap in capitals:
            target_strings.append(cap)

    blacklist = blacklistWords()
    possible = []

    for string in target_strings:
        if (string):
            # reformat string
            string = removeBadCharacters(string)

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

    sorted_results = sorted(results, key = lambda i: i['frequency'], reverse=True)
    printFullTable(sorted_results, struct='dictlist')

    if (sendtweet):
        tweetdata = {}
        for r in sorted_results[:10]:
            tweetdata['$' + r['ticker']] = r['frequency']

        headline = "Top mentioned stocks on r/wallstreetbets and times mentioned:\n"
        tweet = headline + translate_data(tweetdata)
        send_tweet(tweet)
        
