import json
import math
import statistics
import sys
from ..core.api.historical import getHistoricalData
from ..core.api.stats import getKeyStats
from ..core.functions import extract_data, logReturns
from .functions import *


def vix_explanation():
    """
    The VIX calculation as explained by Investopedia.
    https://www.investopedia.com/articles/active-trading/070213/tracking-volatility-how-vix-calculated.asp

    1. The first set of numbers to the right of the “=” represents time. This figure is determined by using the time to 
    expiration in minutes of the nearest term option divided by 525,600, which represents the number of minutes in a 365-day 
    year. Assuming the VIX calculation time is 8:30 a.m., the time to expiration in minutes for the 16-day option will be the 
    number of minutes within 8:30 a.m. today and 8:30 a.m. on the settlement day. In other words, the time to expiration 
    excludes midnight to 8:30 a.m. today and excludes 8:30 a.m. to midnight on the settlement day (full 24 hours excluded). The 
    number of days we’ll be working with will technically be 15 (16 days minus 24 hours), so it's 
    15 days x 24 hours x 60 minutes = 21,600. Use the same method to get the time to expiration in minutes for the 44-day option 
    to get 43 days x 24 hours x 60 minutes = 61,920 (Step 4).

    2. The result is multiplied by the volatility of the option, represented in the example by 0.066472.

    3. The result is then multiplied by the result of the difference between the number of minutes to expiration of the next term
     option (61,920) minus the number of minutes in 30 days (43,200). This result is divided by the difference of the number of 
     minutes to expiration of the next term option (61,920) minus the number of minutes to expiration of the near term 
     option (21,600). Just in case you’re wondering where 30 days came from, the VIX uses a weighted average of options with a 
     constant maturity of 30 days to expiration

    4. The result is added to the sum of the time calculation for the second option, which is 61,920 divided by the number of 
    minutes in a 365-day year (526,600). Just as in the first calculation, the result is multiplied by the volatility of the 
    option, represented in the example by 0.063667.

    5. Next we repeat the process covered in step 3, multiplying the result of step 4 by the difference of the number of minutes 
    in 30 days (43,200), minus the number of minutes to expiration of the near-term options (21,600). We divide this result by 
    the difference of the number of minutes to expiration of the next-term option (61,920) minus the number of minutes to 
    expiration of the near-term options (21,600).

    6. The sum of all previous calculations is then multiplied by the result of the number of minutes in a 365-day year 
    (526,600) divided by the number of minutes in 30 days (43,200).

    7. The square root of that number multiplied by 100 equals the VIX.
    """


def vix_calculation(ticker='SPY', sandbox=False):
    """
    Runs the VIX equation on a ticker.

    Parameters
    ----------
    ticker      :string
    sandbox     :bool
                Sets the IEX environment to sandbox mode to make limitless API calls for testing.

    Returns
    -------
    vix         :float
    """
    # asset_data = getHistoricalData(ticker, '1y', priceOnly=True, sandbox=sandbox)
    # prices = list(reversed(extract_data(asset_data, 'close')))

    # Daily logarithmic returns, basically increase on an evenly-scaled percent change basis.
    # log_returns = logReturns(prices)

    # Number of minutes until nearest option expiration date, and number of minutes until next month's expiration date.
    this_month_option, next_month_option = optionExpirationMinutes(ticker)

    # This is a part I don't entirely understand: "The result is multiplied by the volatility of the option". 
    # It will take more research and perhaps access to better data. 
    # I originally tried using the beta obtained from IEX, but instead used the stdev of the log returns using arbitrary 16 & 44
    # day lengths.

    # volatility of 16 days and 44 days
    # vol3Weeks = statistics.stdev(log_returns[:16])
    # monthVol = statistics.stdev(log_returns[:44])

    # Beta
    # beta = getKeyStats(ticker, filterResults=['beta'], sandbox=sandbox)['beta']


    # minutes in year, minutes in month
    min_in_year = 525600
    min_in_month = 43200

    # Vix calculation as explained by Investopedia.
    vix = math.sqrt(
        (this_month_option / min_in_year) * vol3Weeks * (next_month_option - min_in_month / next_month_option - this_month_option) +
        (next_month_option / min_in_year) * monthVol * (min_in_month - this_month_option / next_month_option - this_month_option)
    )

    return vix
