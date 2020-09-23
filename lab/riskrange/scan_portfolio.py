import statistics
import math
import json
from .export import *
from .methodology import *
from ..shared.functions import *
from ..shared.imports import *
from tabulate import tabulate


# portfolio = [
#     'GOLD',
#     'GDXJ',
#     'GDX',
#     'UUUU',
#     'UEC',
#     'DBA',
#     'SILJ',
#     'SLV',
#     'SBSW',
#     'ISVLF',
#     'KNTNF',
# ]

portfolio = [
    'AG',
    'MUX',
    'EGO',
    'AUY',
    'FNV',
    'AAPL',
    'TLT',
    'ISVLF',
    'HL',
    'JPM',
    'PPLT',
    'NEM',
    'MSFT',
    'UUUU',
    'SILJ',
    'GDXJ',
    'F',
    'GOLD',
    'MENEF',
    'SLV',
    'SBSW',
    'GDX',
    'GLD',
    'UEC',
]

signalArray = {}
for ticker in portfolio:
    data = rangeRules(ticker)
    signalArray[ticker] = data[ticker]

    print(tabulate([
        ['technicalHigh', data[ticker]['donchian']['technicalHigh']],
        ['shortTermDonchianHigh', data[ticker]['donchian']['shortTermHigh']],
        ['Current Price', data[ticker]['currentPrice']],
        ['shortTermDonchianLow', data[ticker]['donchian']['shortTermLow']],
        ['technicalLow', data[ticker]['donchian']['technicalLow']],
        ['', ''],
        ['1 Stdev Higher', data[ticker]['vol']['upper']],
        ['Current Price', data[ticker]['currentPrice']],
        ['1 Stdev Lower', data[ticker]['vol']['lower']],
        ['', ''],
        ['Upper Range', data[ticker]['range']['upper']],
        ['Current Price', data[ticker]['currentPrice']],
        ['Lower Range', data[ticker]['range']['lower']],
        ['', ''],
        ['PercentUpside', data[ticker]['range']['upside']],
        ['PercentDownside', data[ticker]['range']['downside']],
        ['ImpliedVol', data[ticker]['vol']['implied']],
        ['ImpliedVol%', data[ticker]['vol']['impliedPercent']],
        ['VolumeChange', data[ticker]['vol']['volumeChange']]],
        headers=[ticker, data[ticker]['signal']]))


writeCSV(signalArray)
