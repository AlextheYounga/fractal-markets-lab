import json
import math
import statistics
import sys
from ..core.api import getHistoricalData
from ..core.functions import extractData
from .functions import *


def vixCalculation(ticker='SPAZF'):
    # Testing Spanish Mountain Gold Stock
    asset_data = getHistoricalData(ticker, '1y')
    prices = list(reversed(extractData(asset_data, 'close')))
    # Daily logarithmic returns, basically increase on an evenly-scaled percent change basis.
    log_returns = logReturns(prices)
    # Number of minutes until nearest option expiration date, and number of minutes until next month's expiration date.
    this_month_option, next_month_option = optionExpirationMinutes()
    # volatility of 16 days and 44 days
    vol3Weeks = statistics.stdev(log_returns[:16])
    monthVol = statistics.stdev(log_returns[:44])
    # minutes in year, minutes in month
    min_in_year = 525600
    min_in_month = 43200

    # Vix calculation as explained by Investopedia.
    vix = math.sqrt(
        (this_month_option / min_in_year) * vol3Weeks * (next_month_option - min_in_month / next_month_option - this_month_option) + 
        (next_month_option / min_in_year) * monthVol * (min_in_month - this_month_option / next_month_option - this_month_option)
        )

    return vix
    # Output = 21.692995685345284