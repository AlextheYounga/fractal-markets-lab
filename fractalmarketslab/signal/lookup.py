import statistics
import math
import json
from ..shared.functions import *
from ..shared.imports import *
from tabulate import tabulate

def calculate(ticker):
    signalArray = {}
    asset_data = getLongTermData(ticker)

    prices = extractData(asset_data, 'close')
    current_price = getCurrentPrice(ticker)
    highs = extractData(asset_data, 'high')
    lows = extractData(asset_data, 'low')
    dates = extractData(asset_data, 'date')
    volumes = extractData(asset_data, 'volume')

    donchianHigh = max(list(reversed(highs))[:16])
    donchianLow = min(list(reversed(lows))[:16])

    stdevTrade = statistics.stdev(list(reversed(prices))[:16])
    stdevMonth = statistics.stdev(list(reversed(prices))[:22])
    stdevTrend = statistics.stdev(list(reversed(prices))[:64])
    volumeTrend = list(reversed(volumes))[:64]
    volumeChange = round(((volumeTrend[0] - volumeTrend[-1]) / volumeTrend[-1])*100, 2) if (volumeTrend[0] != 0 and volumeTrend[-1] != 0) else 0

    impliedVolTrade = prices[-1] * (stdevTrade / prices[-1]) * (math.sqrt(1/16)) if (prices[-1] != 0) else 0
    impliedVolMonth = prices[-1] * (stdevMonth / prices[-1]) * (math.sqrt(1/22)) if (prices[-1] != 0) else 0
    impliedVolTrend = prices[-1] * (stdevTrend / prices[-1]) * (math.sqrt(1/64)) if (prices[-1] != 0) else 0
    impliedVolMean = round(statistics.mean([impliedVolTrade, impliedVolMonth, impliedVolTrend]), 2)
    upperVol = round((prices[-1] + impliedVolMean), 2)
    lowerVol = round((prices[-1] - impliedVolMean), 2)
    highRange = round((donchianHigh - impliedVolMean), 2)
    lowRange = round((donchianLow + impliedVolMean), 2)

    # Signal based on volatility and probability.
    if (upperVol < current_price):
        signal = 'StDev High'
    if (lowerVol > current_price):
        signal = 'StDev Low'
    if (lowerVol <= current_price <= upperVol):
        signal = 'Hold - Within StDev'
    if (lowRange > current_price):
        signal = 'Buy!'
    if (highRange < current_price):
        signal = 'Sell Signal'
    if (donchianLow > current_price):
        signal = 'Donchian Low'
    if (donchianHigh < current_price):
        signal = '3 Week High'

    print(tabulate([
        ['DonchianHigh', donchianHigh],
        ['Current Price', current_price],
        ['DonchianLow', donchianLow],
        ['', ''],
        ['Vol High', upperVol],
        ['Current Price', current_price],
        ['Vol Low', lowerVol],
        ['', ''],
        ['Upper Range', highRange],
        ['Current Price', current_price],
        ['Lower Range', lowRange],
        ['', ''],
        ['ImpliedVol', impliedVolMean],
        ['VolumeChange', '{}%'.format(volumeChange)]],
        headers=[ticker, signal]))

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
            'volumeChange': volumeChange,
        },
        'range': {
            'upper': highRange,
            'lower': lowRange
        }
    }
