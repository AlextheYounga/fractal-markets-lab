import praw
from praw.models import MoreComments
import colored
from colored import stylize
from ..core.functions import frequencyInList
from ..core.api.stats import getQuoteData
import datetime
import re
import sys
import json
import os
import pprint
from ..fintwit.tweet import send_tweet
from dotenv import load_dotenv
load_dotenv()


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

for submission in subreddit.hot(limit=2):
    post_time = datetime.datetime.fromtimestamp(submission.created)
    print(stylize("r/wallstreetbets: " + submission.title + str(post_time), colored.fg("green")))
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

possible_stocks = {}
freqs = []
for string in target_strings:
    if (string):
        # reformat string
        string = str(string)
        if ('$' in string):
            string = string.split('$')[1]
        string = string.strip()

        if ((not string) or (string in possible_stocks.keys())):
            continue

        freq = frequencyInList(target_strings, string)
        freqs.append(freq)        
        possible_stocks[string] = freq

# top_10 = 



        
results = {}
# print(stylize("Searching {}...".format(string), colored.fg("yellow")))
# stock = getQuoteData(string, filterResults=[
#     'symbol',
#     'companyName',
#     'close',
#     'changePercent',
#     'ytdChange',
#     'volume'
# ])
# if (stock):
#     print(stylize("{} stock found".format(string), colored.fg("green")))
#     results[string] = {
#         'stock': stock,
#         'frequency': freq
#     }


print(json.dumps(results, indent=1))
