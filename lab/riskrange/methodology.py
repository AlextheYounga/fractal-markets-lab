import statistics
import math
import json
from ..shared.functions import *
from ..shared.imports import *
from datetime import datetime 


def rangeRules(ticker):
    signalArray = {}
    assetData = getShortTermData(ticker)
    
    # Data
    prices = removeZeroes(extractData(assetData, 'close'))
    current_price = getCurrentPrice(ticker)
    highs = removeZeroes(extractData(assetData, 'high'))
    lows = removeZeroes(extractData(assetData, 'low'))
    dates = removeZeroes(extractData(assetData, 'date'))
    volumes = removeZeroes(extractData(assetData, 'volume'))

    # Technicals
    technicalDonchianHigh = max(list(reversed(highs))[:22])
    technicalDonchianLow = min(list(reversed(lows))[:22])    
    shortDonchianHigh = max(list(reversed(highs))[:16])
    shortDonchianLow = min(list(reversed(lows))[:16])

    # Volatility
    stdevTrade = statistics.stdev(prices[:16])
    stdevMonth = statistics.stdev(prices[:22])
    stdevTrend = statistics.stdev(prices[:64])    
    volTrade = prices[-1] * (stdevTrade / prices[-1]) * (math.sqrt(1/16)) if (prices[-1] != 0) else 0
    volMonth = prices[-1] * (stdevMonth / prices[-1]) * (math.sqrt(1/22)) if (prices[-1] != 0) else 0
    volTrend = prices[-1] * (stdevTrend / prices[-1]) * (math.sqrt(1/64)) if (prices[-1] != 0) else 0    
    volPercent = (volMonth / current_price) * 100
    
    # Volume
    volumeTrend = list(reversed(volumes))[:64]
    volumeChange = ((volumeTrend[0] - volumeTrend[-1]) / volumeTrend[-1]) * 100 if (volumeTrend[0] != 0 and volumeTrend[-1] != 0) else 0
    
    # Probability Range
    upperVol = (prices[-1] + volMonth)
    lowerVol = (prices[-1] - volMonth)
    highRange = (shortDonchianHigh - (volMonth * 2))
    lowRange = (shortDonchianLow + (volMonth * 2))
    percentUpside = ((shortDonchianHigh - current_price) / current_price) * 100 if (technicalDonchianHigh > current_price) else "Infinite"
    percentDownside = ((current_price - shortDonchianLow) / current_price) * 100 if (current_price > technicalDonchianLow) else "Infinite"    

    # Convert to Percentage Format
    volPercent = "{}%".format(round(volPercent, 2))
    volumeChange = "{}%".format(round(volumeChange, 2))
    percentUpside = "{}%".format(round(percentUpside, 2)) if isinstance(percentUpside, float) else percentUpside
    percentDownside = "{}%".format(round(percentDownside, 2)) if isinstance(percentDownside, float) else percentDownside

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
            'shortTermLow': round(shortDonchianLow, 3),
            'shortTermHigh': round(shortDonchianHigh, 3),
            'technicalLow': round(technicalDonchianLow, 3),
            'technicalHigh': round(technicalDonchianHigh, 3)
        },
        'vol': {
            'upper': round(upperVol, 3),
            'lower': round(lowerVol, 3),
            'implied': round(volMonth, 3),
            'impliedPercent': volPercent,
            'volumeChange': volumeChange,
        },
        'range': {
            'upper': round(highRange, 3),
            'lower': round(lowRange, 3),
            'downside': percentDownside,
            'upside': percentUpside,
        }
    }

    return signalArray
