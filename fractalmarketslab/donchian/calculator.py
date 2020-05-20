import statistics
from scipy import stats
from .functions import *
from .imports import *
from .export import exportDonchian
import math
import sys


def calculate(ticker):
    # ticker = "RSP"
    asset_data = getShortApiData(ticker)

    prices = list(reversed(extractData(asset_data, 'close')))
    highs = list(reversed(extractData(asset_data, 'high')))
    lows = list(reversed(extractData(asset_data, 'low')))
    dates = list(reversed(extractData(asset_data, 'date')))

    donchian_range = {
        'donchianHigh': max(highs[:16]),
        'currentPrice': prices[0],
        'donchianLow': min(lows[:16])
    }

    print(json.dumps(donchian_range, indent=1))
    exportDonchian(donchian_range, ticker)
