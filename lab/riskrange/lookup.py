import statistics
import math
import json
from .methodology import *
from ..shared.functions import *
from ..shared.imports import *
from tabulate import tabulate

def rangeLookup(ticker):
    data = rangeRules(ticker)

    print(tabulate([
        ['technicalHigh', data[ticker]['donchian']['technicalHigh']],
        ['shortTermDonchianHigh', data[ticker]['donchian']['week3High']],
        ['Current Price', data[ticker]['currentPrice']],
        ['shortTermDonchianLow', data[ticker]['donchian']['week3Low']],
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
        ['stDev', data[ticker]['vol']['stDev']],
        ['stDevPercent%', data[ticker]['vol']['stDevPercent']],
        ['VolumeChange', data[ticker]['vol']['volumeChange']],
        ['3MonthTrend', data[ticker]['trend']]],
        headers=[ticker, data[ticker]['signal']]))   



