import statistics
import json
from ..core.functions import *
from ..core.api import *
from .export import exportDonchian
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate


def calculate(ticker):
    asset_data = getHistoricalData(ticker, '3m')
        
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
