import json
import os
import sys
from ..core.functions import prompt_yes_no
from dotenv import load_dotenv
import twitter
load_dotenv()

api = twitter.Api(consumer_key=os.environ.get("TWITTER_API_KEY"),
                  consumer_secret=os.environ.get("TWITTER_SECRET_KEY"),
                  access_token_key=os.environ.get("TWITTER_ACCESS_KEY"),
                  access_token_secret=os.environ.get("TWITTER_ACCESS_SECRET"))


def write_headline():
    """Prompt in terminal for tweet headline.
    """
    sys.stdout.write('Write tweet:')
    tweet_headline = input()

    return tweet_headline


def tweet_volume(data):
    headline = write_headline()
    tweet = "{} \n".format(headline)
    for i, stock in enumerate(data):
        ticker = '${}'.format(stock['ticker'])
        previousVolume = stock['previousVolume']
        volume = stock['volume']
        tweet_data = "{} previous: {}, today: {} \n".format(ticker, previousVolume, volume)
        tweet = tweet + tweet_data

    if (len(tweet) <= 280):
        print(tweet)
        confirm = prompt_yes_no('Send Tweet?')
        if (confirm):
            api.PostUpdate(tweet)
            print('Tweet Sent {}'.format(tweet))
    else:
        print('Tweet greater than 280')
