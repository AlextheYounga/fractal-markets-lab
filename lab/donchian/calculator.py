import statistics
import json
from ..core.functions import extractData
from ..core.api import getHistoricalData, testHistoricalData, getCurrentPrice
from .export import exportDonchian
from tabulate import tabulate
from ..twitter.tweet import send_tweet, translate_data
# import matplotlib.pyplot as plt
# import numpy as np


def calculate(ticker, tweet=False):
    # asset_data = getHistoricalData(ticker, '1m')
    asset_data = testHistoricalData(ticker, '1m')

    prices = extractData(asset_data, 'close')
    highs = extractData(asset_data, 'high')
    lows = extractData(asset_data, 'low')
    dates = extractData(asset_data, 'date')

    donchian_range = {
        'donchianHigh': max(list(reversed(highs))[:16]),
        'currentPrice': getCurrentPrice(ticker),
        'donchianLow': min(list(reversed(lows))[:16])
    }

    print(tabulate([
        ['Donchian High', donchian_range['donchianHigh']],
        ['Current Price', donchian_range['currentPrice']],
        ['Donchian Low', donchian_range['donchianLow']]]))

    if (tweet):
        headline = "${} 3week Donchian Range:".format(ticker)
        tweet = headline + translate_data(donchian_range)
        send_tweet(tweet)

