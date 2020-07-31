import statistics
import json
import sys
from .functions import *
from ..shared.functions import *
from ..shared.api import *
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate
from collections import OrderedDict 


def analyze(ticker):
    asset_data = testShortTermPrices(ticker)
    data_inversed = OrderedDict(reversed(list(asset_data.items())))
    
    prices = extractData(asset_data, 'close')
    highs = extractData(asset_data, 'high')
    lows = extractData(asset_data, 'low')
    dates = extractData(asset_data, 'date')
    
    upStreaks, downStreaks = longestStretch(data_inversed)
    print(json.dumps(upStreaks, indent=1))
    # trend_data = trendAnalysis(list(reversed(prices))[:64])
    # upStreak, downStreak = longestStretch(list(reversed(prices))[:64])

    # print("\n")
    # print(tabulate([
    #     ['Count', trend_data['upDays']['count']],
    #     ['Consecutive', trend_data['upDays']['consecutive']],
    #     ['Longest Stretch', upStreak],
    #     ['Average', trend_data['upDays']['average']]],
    #     headers=['Up Days', '']))

    # print("\n")
    # print(tabulate([
    #     ['Count', trend_data['downDays']['count']],
    #     ['Consecutive', trend_data['downDays']['consecutive']],
    #     ['Longest Stretch', downStreak],
    #     ['Average', trend_data['downDays']['average']]],
    #     headers=['Down Days', '']))


