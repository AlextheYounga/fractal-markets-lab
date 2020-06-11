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
    # ticker = "RSP"
    asset_data = getShortApiData(ticker)
    
    prices = extractData(asset_data, 'close')
    highs = extractData(asset_data, 'high')
    lows = extractData(asset_data, 'low')
    dates = extractData(asset_data, 'date')

    donchian_range = {
        'donchianHigh': max(list(reversed(highs))[:16]),
        'currentPrice': list(reversed(prices))[0],
        'donchianLow': min(list(reversed(lows))[:16])
    }

    print(json.dumps(donchian_range, indent=1))
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
