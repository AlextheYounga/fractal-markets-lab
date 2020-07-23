import statistics
import json
from ..shared.api import *
from ..shared.functions import *
from tabulate import tabulate


def calculate(ticker):
    asset_data = getLongTermPrices(ticker)
    current_price = getCurrentPrice(ticker)
    prices = extractData(asset_data, 'close')

    trade_stdev = statistics.stdev(list(reversed(prices))[:16])
    month_stdev = statistics.stdev(list(reversed(prices))[:22])
    trend_stdev = statistics.stdev(list(reversed(prices))[:64])

    print(tabulate([
        ['Trade', trade],
        ['Month', month],
        ['Trend', trend]],           
        headers=['Scale', 'StDev']))