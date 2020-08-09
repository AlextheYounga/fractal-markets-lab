import json
import math
import statistics
import sys
from ..shared.imports import *
from ..shared.functions import *


def calculateVol(ticker):
    asset_data = getLongTermPrices(ticker)
    prices = list(reversed(extractData(asset_data, 'close')))
    log_returns = logReturns(prices)

    stdevTrade = statistics.stdev(list(reversed(prices))[:16])
    stdevMonth = statistics.stdev(list(reversed(prices))[:22])
    stdevTrend = statistics.stdev(list(reversed(prices))[:64])
