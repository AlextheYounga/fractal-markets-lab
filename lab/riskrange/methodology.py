import statistics
import sys
import math
import json
from ..core.functions import extract_data, removeZeroes
from ..core.api.historical import getHistoricalData
from ..core.api.stats import getCurrentPrice
from datetime import datetime


def rangeRules(ticker):
    signalArray = {}
    assetData = getHistoricalData(ticker, timeframe='3m')    
    # --------------------------------------------
    # Data
    prices = list(reversed(removeZeroes(extract_data(assetData, 'close'))))
    current_price = getCurrentPrice(ticker)
    highs = list(reversed(removeZeroes(extract_data(assetData, 'high'))))
    lows = list(reversed(removeZeroes(extract_data(assetData, 'low'))))
    dates = list(reversed(removeZeroes(extract_data(assetData, 'date'))))
    volumes = list(reversed(removeZeroes(extract_data(assetData, 'volume'))))
    # --------------------------------------------

