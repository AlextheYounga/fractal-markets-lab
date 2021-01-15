from dotenv import load_dotenv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pylab
from .gold import read_historical_gold_prices
from ..core.functions import extract_data
import os
import sys
from..core.api import getHistoricalData
load_dotenv()


def price_in_gold(ticker, timespan='5y', test=False):
    if (test):
        asset_prices = getHistoricalData(ticker, timespan, False, sandbox=True)
    else:
        asset_prices = getHistoricalData(ticker, timespan)

    gold_prices = read_historical_gold_prices()

    dates = []
    prices = []
    for day in asset_prices:
        price = float(day['close'] / gold_prices[day['date']]) if (day['date'] in gold_prices) else 0
        dates.append(day['date'])
        prices.append(round(price, 3))


    x = dates

    plt.plot(x, prices, label='price/oz')  # etc.    
    plt.xlabel('x Date')
    plt.ylabel('y Price')
    plt.title("{} Priced in Gold".format(ticker))
    plt.legend()

    plt.show()
