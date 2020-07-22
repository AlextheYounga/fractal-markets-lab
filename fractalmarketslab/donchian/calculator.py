import statistics
import json
from .functions import *
from ..shared.functions import *
from .imports import *
from .export import exportDonchian
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate


def calculate(ticker):
    asset_data = getShortTermPrices(ticker)
        
    prices = extractData(asset_data, 'close')
    highs = extractData(asset_data, 'high')
    lows = extractData(asset_data, 'low')
    dates = extractData(asset_data, 'date')

    trend_data = trendAnalysis(list(reversed(prices))[:22])
    upStreak, downStreak = longestStretch(prices)

    donchian_range = {
        'donchianHigh': max(list(reversed(highs))[:16]),
        'currentPrice': getCurrentPrice(ticker),
        'donchianLow': min(list(reversed(lows))[:16])
    }
    
    print(tabulate([
        ['Donchian High', donchian_range['donchianHigh']],
        ['Current Price', donchian_range['currentPrice']],
        ['Donchian Low', donchian_range['donchianLow']]]))

    print("\n")
    print(tabulate([
        ['Count', trend_data['upDays']['count']],
        ['Consecutive', trend_data['upDays']['consecutive']],
        ['Longest Stretch', upStreak],
        ['Average', trend_data['upDays']['average']]],
        headers=['Up Days', '']))

    print("\n")
    print(tabulate([
        ['Count', trend_data['downDays']['count']],
        ['Consecutive', trend_data['downDays']['consecutive']],
        ['Longest Stretch', downStreak],
        ['Average', trend_data['downDays']['average']]],
        headers=['Down Days', '']))

    exportDonchian(donchian_range, ticker)

    x = dates
    plt.plot(x, lows, label='lows')  # Plot some data on the (implicit) axes.
    plt.plot(x, prices, label='price')  # etc.
    plt.plot(x, highs, label='highs')
    plt.xlabel('x Date')
    plt.ylabel('y Price')
    plt.title("Donchian")
    plt.legend()

    plt.show()
