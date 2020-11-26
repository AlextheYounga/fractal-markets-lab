import statistics
import json
import sys
from .functions import *
from ...core.functions import *
from ...core.api import *
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate
from collections import OrderedDict 


def streak_analyzer(ticker):
    asset_data = getHistoricalData(ticker, '1yr')
    data_inversed = OrderedDict(reversed(list(asset_data.items())))
    
    prices = extractData(asset_data, 'close')
    dates = extractData(asset_data, 'date')
    
    upStreaks, downStreaks = longestStretch(data_inversed)
    trend_data = trendAnalysis(list(reversed(prices))[:64])



    print("\n")
    print(tabulate([
        ['Count', trend_data['upDays']['count']],
        ['Consecutive', trend_data['upDays']['consecutive']],
        ['Longest Streak', len(upStreaks)],
        ['Average', trend_data['upDays']['average']]],
        headers=['Up Days', '']))

    print("\n")
    print(tabulate([
        ['Count', trend_data['downDays']['count']],
        ['Consecutive', trend_data['downDays']['consecutive']],
        ['Longest Streak', len(downStreaks)],
        ['Average', trend_data['downDays']['average']]],
        headers=['Down Days', '']))
    print("\n")

    print("Up")
    for i, day in upStreaks.items():
        print("{} - {}".format(day['date'], day['close']))

    print("\n")
    print("Down")
    for i, day in downStreaks.items():
        print("{} - {}".format(day['date'], day['close']))

    
   


