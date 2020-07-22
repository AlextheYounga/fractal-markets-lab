import statistics
import json
from ..shared.functions import *
from ..shared.api import *
from tabulate import tabulate

portfolio = [
    'AG',
    'AUMN',
    'GDX',
    'GLD',
    'GOLD',
    'HL',
    'JPM',
    'MSFT',
    'SBSW',
    'SLV',
    'UBER',
    'VXX',
    'WKHS',
    'CVNA'
]

for ticker in portfolio:
    asset_data = getLongTermData(ticker)
        
    prices = extractData(asset_data, 'close')
    current_price = getCurrentPrice(ticker)
    highs = extractData(asset_data, 'high')
    lows = extractData(asset_data, 'low')
    dates = extractData(asset_data, 'date')

    tradeDonchian = {
        'donchianHigh': max(list(reversed(highs))[:16]),
        'donchianLow': min(list(reversed(lows))[:16])
    }

    trendDonchian = {
        'donchianHigh': max(list(reversed(highs))[:64]),
        'donchianLow': min(list(reversed(lows))[:64])
    }

    stdevTrade = statistics.stdev(list(reversed(prices))[:22])

    # Signal based on volatility and probability.
    if (tradeDonchian['donchianHigh'] < current_price):
        signal = 'Sell'
    if (tradeDonchian['donchianLow'] > current_price):
        signal = 'Buy'
    if (tradeDonchian['donchianLow'] > current_price):
        signal = 'Hold'

    # stdevTrade = statistics.stdev(list(reversed(prices))[:22])
    # stdevTrend = statistics.stdev(list(reversed(prices))[:64])
    
    print(tabulate([
        ['DonchianHigh', tradeDonchian['donchianHigh']],
        ['Current Price', current_price],
        ['DonchianLow', tradeDonchian['donchianLow']]],
        headers=['Trade', ticker, 'Signal']))    
    print(tabulate([
        ['DonchianHigh', trendDonchian['donchianHigh']],
        ['Current Price', current_price],
        ['DonchianLow', trendDonchian['donchianLow']]],
        headers=['Trend', ticker, 'Signal']))
    print("\n")

