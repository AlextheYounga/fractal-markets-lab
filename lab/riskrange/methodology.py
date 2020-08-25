import statistics
import math
import json
from ..shared.functions import *
from ..shared.imports import *
from datetime import datetime 


def rangeRules(ticker):
    signalArray = {}
    assetData = getShortTermData(ticker)
    

    prices = removeZeroes(extractData(assetData, 'close'))
    current_price = getCurrentPrice(ticker)
    highs = removeZeroes(extractData(assetData, 'high'))
    lows = removeZeroes(extractData(assetData, 'low'))
    dates = removeZeroes(extractData(assetData, 'date'))
    volumes = removeZeroes(extractData(assetData, 'volume'))

    technicalDonchianHigh = max(list(reversed(highs))[:22])
    technicalDonchianLow = min(list(reversed(lows))[:22])    
    shortDonchianHigh = max(list(reversed(highs))[:8])
    shortDonchianLow = min(list(reversed(lows))[:8])
    # vol = calculateVol(list(reversed(prices)))
    stdevTrade = statistics.stdev(prices[:16])
    stdevMonth = statistics.stdev(prices[:22])
    stdevTrend = statistics.stdev(prices[:64])    
    volTrade = prices[-1] * (stdevTrade / prices[-1]) * (math.sqrt(1/16)) if (prices[-1] != 0) else 0
    volMonth = prices[-1] * (stdevMonth / prices[-1]) * (math.sqrt(1/22)) if (prices[-1] != 0) else 0
    volTrend = prices[-1] * (stdevTrend / prices[-1]) * (math.sqrt(1/64)) if (prices[-1] != 0) else 0
    volMean = round(statistics.mean([volTrade, volMonth, volTrend]), 3)
    volPercent = round((volMean / current_price) * 100)
    
    volumeTrend = list(reversed(volumes))[:64]
    volumeChange = round(((volumeTrend[0] - volumeTrend[-1]) / volumeTrend[-1])*100, 3) if (volumeTrend[0] != 0 and volumeTrend[-1] != 0) else 0
    
    upperVol = (prices[-1] + volMonth)
    lowerVol = (prices[-1] - volMonth)
    highRange = (shortDonchianHigh - volMonth)
    lowRange = (shortDonchianLow + volMonth)
    percentUpside = "{}%".format(round(((shortDonchianHigh - current_price) / current_price) * 100)) if (technicalDonchianHigh > current_price) else "Infinite"
    percentDownside = "{}%".format(round(((current_price - shortDonchianLow) / current_price) * 100)) if (current_price > technicalDonchianLow) else "Infinite"    

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
    if (technicalDonchianLow > current_price):
        signal = 'Donchian Low Breached; Potential Breakout'
    if (technicalDonchianHigh < current_price):
        signal = 'Donchian High Breached; Potential Breakout'

    signalArray[ticker] = {
        'currentPrice': current_price,
        'signal': signal,
        'donchian': {
            'shortTermLow': shortDonchianLow,
            'shortTermHigh': shortDonchianHigh,
            'technicalLow': technicalDonchianLow,
            'technicalHigh': technicalDonchianHigh
        },
        'vol': {
            'upper': upperVol,
            'lower': lowerVol,
            'implied': volMean,
            'impliedPercent': volPercent,
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
