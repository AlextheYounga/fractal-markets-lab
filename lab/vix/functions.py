import json
import sys
from datetime import date, datetime, timedelta
from pytz import timezone
from dateutil.relativedelta import relativedelta
from ..core.api.options import getExpirations
import pandas as pd
import numpy as np
import calendar


def optionExpirationMinutes(ticker):
    """
    Fetches all option expiration dates from api. 
    Finds this month's expiration and next months expiration.
    Calculates and returns the difference (in seconds) from those expiration dates and today. 
    """
    optionExps = getExpirations(ticker, sandbox=True)
    today = timezone('US/Eastern').localize(datetime.now())
    year = today.year
    month = today.month
    next_month = (today + relativedelta(months=+1)).month
    this_month_options = {}
    next_month_options = {}


    for exp in optionExps:
        expDate = datetime.strptime(exp, '%Y%m%d')
        expMonth = expDate.month
        expYear = expDate.year

        # Finding this and next month's closest option expiration dates.
        if ((month == expMonth) and (year == expYear)):
            opt = timezone('US/Eastern').localize(expDate).replace(hour=8, minute=30)
            # https://www.optionseducation.org/referencelibrary/white-papers/page-assets/vixwhite.aspx
            # TODO: if (diff > 7)
            diff = opt - today
            print(diff)
            sys.exit()
            this_month_options[diff] = opt

        if ((next_month == expMonth) and (year == expYear)):
            opt = timezone('US/Eastern').localize(expDate).replace(hour=8, minute=30)
            diff = opt - today

            next_month_options[diff] = opt
    
    this_month_expir = this_month_options[min(this_month_options.keys())]
    next_month_expir = next_month_options[min(next_month_options.keys())]


    if (this_month_expir and next_month_expir):        
        this_month_calc = this_month_expir - today #Calculating difference
        this_month_diff = int((this_month_calc.total_seconds() // 60) - 1440) #Converting difference to seconds

        next_month_calc = next_month_expir - today #Calculating difference
        next_month_diff = int((next_month_calc.total_seconds() // 60) - 1440) #Converting difference to seconds

        return this_month_diff, next_month_diff
    else:
        print('Failed to fetch option expiration dates. Closing program...')
        sys.exit()


def interdayReturns(prices):
    int_returns = []
    for i, price in enumerate(prices):
        ret = (prices[i + 1] / price) - 1 if (i + 1 in range(-len(prices), len(prices)) and float(prices[i + 1]) != 0) else 0
        int_returns.append(ret)

    return int_returns
