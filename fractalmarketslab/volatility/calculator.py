import statistics
import json
from ..imports.api import *
from .functions import *
from tabulate import tabulate


def calculate(ticker):
    asset_data = getLongTermPrices(ticker)
    current_price = getCurrentPrice(ticker)
    prices = extractData(asset_data, 'close')

    trade = statistics.stdev(list(reversed(prices))[:16])
    month = statistics.stdev(list(reversed(prices))[:22])
    trend = statistics.stdev(list(reversed(prices))[:64])
    tail = statistics.stdev(list(reversed(prices))[:757])
    # fullSeries = statistics.stdev(list(reversed(prices)))

    print(tabulate([
        ['Trade', trade],
        ['Month', month],
        ['Trend', trend],
        ['Tail', tail]],        
        headers=['Scale', 'StDev']))