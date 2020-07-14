import statistics
from scipy import stats
import json
from .functions import *
from .imports import *
from .export import exportDonchian
import math
import sys
import matplotlib.pyplot as plt
import numpy as np


def calculate(ticker):
    asset_data = getShortApiData(ticker)
    
    prices = extractData(asset_data, 'close')
    highs = extractData(asset_data, 'high')
    lows = extractData(asset_data, 'low')
    dates = extractData(asset_data, 'date')

    trend_data = trendAnalysis(list(reversed(prices[:22])))

    donchian_range = {
        'donchianHigh': max(list(reversed(highs))[:16]),
        'currentPrice': getCurrentPrice(ticker),
        'donchianLow': min(list(reversed(lows))[:16])
    }

    print(json.dumps(donchian_range, indent=1))    
    print(json.dumps(trend_data, indent=1))
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
