import statistics
import math
import json
from .export import *
from .methodology import *
from ..shared.functions import *
from ..shared.imports import *
from tabulate import tabulate


portfolio = [
    'PHYS',
    'F',
    'KGC',
    'SPY',
    'AG',
    'GDX',
    'AUY',
    'GDXJ',
    'GLD',
    'GOLD',
    'SPAZF',
    'CNSUF',
    'AUMN',
    'HL',
    'MUX',
    'JPM',
    'MSFT',
    'EGO',
    'NEM',
    'FNV',
    'SBSW',
    'SLV',
    'UBER',
    'WKHS',
    'TLT',
    'CVNA',
    'ISVLF'
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
