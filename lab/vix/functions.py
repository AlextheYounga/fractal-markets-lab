import json
import sys
import datetime
from pytz import timezone
from dateutil.relativedelta import relativedelta
from ..core.api.options import *
import pandas as pd
import numpy as np
import calendar


def calculateOptionExpirations(ticker):
    """
    1. Fetches all option expiration dates from IEX api. 
    2. Finds this month's expiration and next months expiration (the near-term and next-term expirations).
    3. Calculates and returns a dict containing the expiration dates, the time-to-expiration in days as well as 
    seconds.
    """

    today = timezone('US/Central').localize(datetime.now())
    # "...and reflect prices observed at the open of trading – 8:30 a.m. Chicago time."
    # https://www.optionseducation.org/referencelibrary/white-papers/page-assets/vixwhite.aspx

    # Step 1: Fetch all expiration dates from IEX
    optionExps = getExpirations(ticker, sandbox=True)

    # Just some simple variables we will need.
    year = today.year
    month = today.month
    next_month = (today + relativedelta(months=+1)).month
    near_term_options = {}
    next_term_options = {}
    results = {}

    # Step 2: Finding this and next month's closest option expiration dates in Chicago Central Time.
    for exp in optionExps:
        expDate = datetime.strptime(exp, '%Y%m%d')
        expMonth = expDate.month
        expYear = expDate.year

        if ((month == expMonth) and (year == expYear)):
            option = timezone('US/Central').localize(expDate).replace(hour=8, minute=30)  # Forcing expiration date to 8:30am

            # “Near-term” options must have at least one week to expiration; a requirement
            # intended to minimize pricing anomalies that might occur close to expiration.
            # https://www.optionseducation.org/referencelibrary/white-papers/page-assets/vixwhite.aspx

            timeDiff = option - today
            days = abs(timeDiff.days)

            if (days > 7):  # Must be at least 7 days from expiration.
                seconds = int((timeDiff.total_seconds() // 60) - 1440)

                # Adding date and timeInDays to list of next month's options using seconds as key.
                near_term_options[seconds] = [option, days]

        if ((next_month == expMonth) and (year == expYear)):
            option = timezone('US/Central').localize(expDate).replace(hour=8, minute=30)  # Forcing expiration date to 8:30am
            timeDiff = option - today
            days = abs(timeDiff.days)
            seconds = int((timeDiff.total_seconds() // 60) - 1440)

            if (days > 30):  # Generally at least 30 days from expiration.
                seconds = int((timeDiff.total_seconds() // 60) - 1440)

                # Adding date and timeInDays to list of next month's options using seconds as key.
                next_term_options[seconds] = [option, days]

    # Step 3: Calculating the nearest option of each group of options, finding min() value of each group's keys, which
    # again, are the time to expiration in seconds.

    results = {
        'nearTerm': {
            'expirationDate': near_term_options[min(near_term_options.keys())][0],
            'timeInSeconds': min(near_term_options.keys()),
            'timeInDays': near_term_options[min(near_term_options.keys())][1]
        },
        'nextTerm': {
            'expirationDate': next_term_options[min(next_term_options.keys())][0],
            'timeInSeconds': min(next_term_options.keys()),
            'timeInDays': next_term_options[min(next_term_options.keys())][1]
        }
    }

    return results


def calculateF(ticker, expirations, sandbox=False):
    """
    Test
    """
    nearTermExpir = expirations['nearTerm']['expirationDate']
    nextTermExpir = expirations['nextTerm']['expirationDate']
    print(type(nearTermExpir))

    chain = getOptionChain(ticker, nearTermExpir, sandbox)
    print(json.dumps(chain, indent=1))

    # for term in [nearTermExpir, nextTermExpir]:
    #     chain = getOptionChain(ticker, term, sandbox)
