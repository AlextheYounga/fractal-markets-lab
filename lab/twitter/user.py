from django.core.cache import cache
from datetime import datetime, timedelta
from ..core.functions import prompt_yes_no, wordVariator
from time import sleep
from dotenv import load_dotenv
import os
import json
import sched
import time
import logging
import sys
import tweepy
import texttable
load_dotenv()

auth = tweepy.OAuthHandler(os.environ.get("TWITTER_API_KEY"), os.environ.get("TWITTER_SECRET_KEY"))
auth.set_access_token(os.environ.get("TWITTER_ACCESS_KEY"), os.environ.get("TWITTER_ACCESS_SECRET"))

api = tweepy.API(auth)


def autoFollowFollowers(handle, p=0):
    user = api.get_user(handle)
    print("Name: {}\nScreen Name: {}\nDescription: {}\n".format(user.name, user.screen_name, user.description))

    if (prompt_yes_no("This user?")):

        def limit_handled(cursor):
            while True:
                try:
                    yield cursor.next()
                except tweepy.RateLimitError:
                    last_run = cache.get('auto_followers_last_run')
                    current_time = datetime.now()
                    if (last_run):
                        next_run = (last_run + timedelta(minutes=15))
                        wait_time = (next_run - current_time).seconds + 5  # Giving it a little leeway of 5 seconds
                        print("Run Halted =", last_run.strftime("%H:%M:%S"))
                        print("Next Run = {}".format(next_run.strftime("%H:%M:%S")))

                        time.sleep(wait_time)
                    else:
                        print('Halt time not being cached.')
                        wait_time = (15 * 60)
                        next_run = (current_time + timedelta(minutes=15)).strftime("%H:%M:%S")
                        print("Run Stopped =", current_time.strftime("%H:%M:%S"))
                        print("Next Run = {}".format(next_run))

                        time.sleep(wait_time)

        for page in limit_handled(tweepy.Cursor(api.followers, id=user.id, page=p).pages()):
            p += 1
            current_time = datetime.now()
            cache.set('auto_followers_last_run', current_time, 1800)

            print('Page {}'.format(p))
            for f in page:
                if (screen_follower(f)):
                    try:
                        friendship = api.lookup_friendships([f.id])[0]
                    except:
                        break
                    if (not(friendship.is_following or friendship.is_following_requested)):
                        api.create_friendship(f.id, screen_name=None, user_id=f.id, follow=False)
                        print("{} - {} followers".format(f.screen_name, f.followers_count))


def check_bio(bio):
    base_words = [
        'stock'
        'market',
        'gold',
        'commodities',
        'data',
        'economy',
        'bitcoin',
        'crypto',
        'silver',
        'commodity',
        'trade',
        'trading',
        'research',
        'hedge',
        'accounting',
        'machine',
        'learning',
        'coding',
        'MBA',
        'CFA',
        'business',
        'capitalism',
        'libertarian',
        'option',
        'developer',        
        'programmer'
    ]
    keywords = wordVariator(base_words)

    for k in keywords:
        if (k in bio):
            return True

    return False


def screen_follower(f):
    if (f.followers_count > 300):
        if (check_bio(f.description)):
            return True
    return False