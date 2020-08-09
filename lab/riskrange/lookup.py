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
        ['DonchianHigh', data[ticker]['donchian']['high']],
        ['Current Price', data[ticker]['currentPrice']],
        ['DonchianLow', data[ticker]['donchian']['low']],
        ['', ''],
        ['Vol High', data[ticker]['vol']['upper']],
        ['Current Price', data[ticker]['currentPrice']],
        ['Vol Low', data[ticker]['vol']['lower']],
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



