import json
import os
import sys
from ..core.functions import prompt_yes_no
from dotenv import load_dotenv
import twitter
import texttable
load_dotenv()

api = twitter.Api(consumer_key=os.environ.get("TWITTER_API_KEY"),
                  consumer_secret=os.environ.get("TWITTER_SECRET_KEY"),
                  access_token_key=os.environ.get("TWITTER_ACCESS_KEY"),
                  access_token_secret=os.environ.get("TWITTER_ACCESS_SECRET"))

def draw_box(text):
    lines = text.splitlines()
    width = max(len(s) for s in lines)
    res = ['┌' + '─' * width + '┐']
    for s in lines:
        res.append('│' + (s + ' ' * width)[:width] + '│')
    res.append('└' + '─' * width + '┘')
    return '\n'.join(res)


def send_tweet(tweet, headline=True, footer=False):
    while True:
        if (headline):
            sys.stdout.write('Write tweet headline:')
            headline = "{} \n".format(input())
            tweet = headline + tweet
        if (footer):
            sys.stdout.write('Write tweet footer:')
            headline = "{} \n".format(input())
            tweet = tweet + headline


        
        print("Tweet:")
        print(draw_box(tweet))
        print('Characters: {}'.format(len(tweet)))

        if (len(tweet) > 280):
            print('Tweet over 280 characters.')
            continue

        while True:
            # First prompt
            send = str(input('Send Tweet? (y/n): '))
            if send in ('y', 'n'):
                break
            print("invalid input.")

        if (send == 'n'):
            while True:
                # Rerun program?
                rerun = str(input('Rerun program? (y/n): '))
                if rerun in ('y', 'n'):
                    break
                else:
                    print("invalid input.")
            if (rerun == 'n'):
                sys.exit()
            else:
                continue
        if (send == 'y'):
            api.PostUpdate(tweet)
            print('Tweet Sent')
            break
