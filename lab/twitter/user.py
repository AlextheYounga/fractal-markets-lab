import os
import json
import sched
import time
import logging
import sys
from time import sleep
from ..core.cron import RepeatedTimer
from ..core.functions import prompt_yes_no
from dotenv import load_dotenv
import tweepy
import texttable
load_dotenv()

auth = tweepy.OAuthHandler(os.environ.get("TWITTER_API_KEY"), os.environ.get("TWITTER_SECRET_KEY"))
auth.set_access_token(os.environ.get("TWITTER_ACCESS_KEY"), os.environ.get("TWITTER_ACCESS_SECRET"))

api = tweepy.API(auth)


def autoFollowFollowers(handle):
    user = api.get_user(handle)
    print("Name: {}\nScreen Name: {}\nDescription: {}\n".format(user.name, user.screen_name, user.description))

    if (prompt_yes_no("This user?")):

        def limit_handled(cursor):
            while True:
                try:
                    yield cursor.next()
                except tweepy.RateLimitError:
                    time.sleep(15 * 60)

        p = 0
        for page in limit_handled(tweepy.Cursor(api.followers, id=user.id).pages()):
            p += 1
            print('Page {}'.format(p))
            for f in page:
                if (f.followers_count > 1000):
                    friendship = api.lookup_friendships([f.id])[0]
                    if (not(friendship.is_following or friendship.is_following_requested)):
                        api.create_friendship(f.id, screen_name=None, user_id=f.id, follow=False)
                        print("{} - {} followers".format(f.screen_name, f.followers_count))