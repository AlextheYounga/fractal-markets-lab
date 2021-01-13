import json
import sys
from ..core.functions import extract_data
from ..core.api import getHistoricalData, getCurrentPrice
from .export import exportDonchian
from ..core.output import printTable
from ..fintwit.tweet import send_tweet, translate_data


def calculate(ticker, tweet=False):
    asset_data = getHistoricalData(ticker, '1m')

    prices = extract_data(asset_data, 'close')
    highs = extract_data(asset_data, 'high')
    lows = extract_data(asset_data, 'low')
    dates = extract_data(asset_data, 'date')

    donchian_range = {
        'donchianHigh': max(list(reversed(highs))[:16]),
        'currentPrice': getCurrentPrice(ticker),
        'donchianLow': min(list(reversed(lows))[:16])
    }

    printTable(donchian_range)

    if (tweet):
        headline = "${} 3week Donchian Range:".format(ticker)
        tweet = headline + translate_data(donchian_range)
        send_tweet(tweet)

