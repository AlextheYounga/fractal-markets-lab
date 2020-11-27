import django
from ..core.api import getCurrentPrice
from django.apps import apps
import requests
import json
import sys
import os
from dotenv import load_dotenv
from ..twitter.tweet import send_tweet
load_dotenv()
django.setup()


def getETFs(tickersonly=False):
    Stock = apps.get_model('database', 'Stock')
    stocks = Stock.objects.all()
    etfs = []
    for stock in stocks:
        if ('ETF' in stock.name):
            if (tickersonly):
                etfs.append(stock.ticker)
            else:
                etfs.append(stock)

    return etfs

def getTopPerformingETFs(n=None):
    """
    Parameters
    ----------
    n      :int
            number of items you wish to take

    Returns
    -------
    query object
    """
    MacroTrends = apps.get_model('database', 'MacroTrend')
    if (n):
        trends = MacroTrends.objects.order_by('-ytdChangePercent')[:n]
    else:
        trends = MacroTrends.objects.order_by('-ytdChangePercent')
    
    return trends


def top_performing_etf_tweet():
    tweet = ""
    for etf in getTopPerformingETFs(5):
        txt = "${} +{}%\n".format(etf.ticker, round(etf.ytdChangePercent, 2))
        tweet = tweet + txt
    send_tweet(tweet, True)
    
    