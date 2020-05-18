import statistics
from scipy import stats
from .functions import *
from .imports import *
import math
import sys


ticker = "GDX"
asset_data = getShortApiData(ticker)

prices = list(reversed(extractData(asset_data, 'close')))
highs = list(reversed(extractData(asset_data, 'high')))
lows = list(reversed(extractData(asset_data, 'low')))
dates = list(reversed(extractData(asset_data, 'date')))

donchian_stats = {
    'donchianHigh': max(highs[:16]),
    'currentPrice': prices[0],
    'donchianLow': min(lows[:16])
}

print(json.dumps(donchian_stats, indent=1))

# =IF($K8<>"",MAX(OFFSET($K8,-MIN($A8,$M$1),0):$K8),"")