import statistics
import math
import json
from ..shared.functions import *
from ..shared.imports import *
from datetime import datetime 


def calculate_signals(ticker):
    signalArray = {}
    assetData = getLongTermData(ticker)

    prices = removeZeroes(extractData(assetData, 'close'))
    current_price = getCurrentPrice(ticker)
    highs = removeZeroes(extractData(assetData, 'high'))
    lows = removeZeroes(extractData(assetData, 'low'))
    dates = removeZeroes(extractData(assetData, 'date'))
    volumes = removeZeroes(extractData(assetData, 'volume'))

    donchianHigh = max(list(reversed(highs))[:8])
    donchianLow = min(list(reversed(lows))[:8])

    stdevTrade = statistics.stdev(list(reversed(prices))[:16])
    stdevMonth = statistics.stdev(list(reversed(prices))[:22])
    stdevTrend = statistics.stdev(list(reversed(prices))[:64])
    volumeTrend = list(reversed(volumes))[:64]
    volumeChange = round(((volumeTrend[0] - volumeTrend[-1]) / volumeTrend[-1])*100, 3) if (volumeTrend[0] != 0 and volumeTrend[-1] != 0) else 0

    impliedVolTrade = prices[-1] * (stdevTrade / prices[-1]) * (math.sqrt(1/16)) if (prices[-1] != 0) else 0
    impliedVolMonth = prices[-1] * (stdevMonth / prices[-1]) * (math.sqrt(1/22)) if (prices[-1] != 0) else 0
    impliedVolTrend = prices[-1] * (stdevTrend / prices[-1]) * (math.sqrt(1/64)) if (prices[-1] != 0) else 0
    impliedVolMean = round(statistics.mean([impliedVolTrade, impliedVolMonth, impliedVolTrend]), 3)
    impliedVolPercent = round((impliedVolMean / current_price) * 100)
    upperVol = (prices[-1] + impliedVolMonth)
    lowerVol = (prices[-1] - impliedVolMonth)
    highRange = (donchianHigh - impliedVolMonth)
    lowRange = (donchianLow + impliedVolMonth)
    percentUpside = "{}%".format(round(((donchianHigh - current_price) / current_price) * 100)) if (donchianHigh > current_price) else "Infinite"
    percentDownside = "{}%".format(round(((current_price - donchianLow) / current_price) * 100)) if (current_price > donchianLow) else "Infinite"

    # Signal based on volatility and probability.
    if (upperVol < current_price):
        signal = '~1 Stdev Higher'
    if (lowerVol > current_price):
        signal = '~1 Stdev Lower'
    if (lowerVol <= current_price <= upperVol):
        signal = 'Hold - Within StDev'
    if (lowRange > current_price):
        signal = 'Buy!'
    if (highRange < current_price):
        signal = 'Sell Signal'
    if (donchianLow > current_price):
        signal = 'Donchian Low'
    if (donchianHigh < current_price):
        signal = 'Above Donchian High'

    signalArray[ticker] = {
        'currentPrice': current_price,
        'signal': signal,
        'donchian': {
            'low': donchianLow,
            'high': donchianHigh
        },
        'vol': {
            'upper': upperVol,
            'lower': lowerVol,
            'implied': impliedVolMean,
            'impliedPercent': impliedVolPercent,
            'volumeChange': volumeChange,
        },
        'range': {
            'upper': highRange,
            'lower': lowRange,
            'downside': percentDownside,
            'upside': percentUpside
        }
    }

    return signalArray
