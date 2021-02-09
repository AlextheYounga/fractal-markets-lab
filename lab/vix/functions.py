import json
import sys
import datetime
import time
import calendar
from math import e
from pytz import timezone
from dateutil.relativedelta import relativedelta
from ..core.api.options import *
import pandas as pd
import numpy as np
import calendar


def collectOptionChain(ticker, testing=True):
    today = datetime.datetime.now()
    year = today.year
    month = today.month
    next_month = (today + relativedelta(months=+1)).month
    next_month_year = (today + relativedelta(months=+1)).year
    next_month_end = calendar.monthrange(next_month_year, next_month)[1]
    

    # Building a timerange to send to TD Ameritrade's API
    fromDate = today
    toDate = datetime.datetime(next_month_year, next_month, next_month_end)
    timeRange = [fromDate, toDate]

    """ Step 1: Fetch the option chain from TD Ameritrade """
    
    if (testing):
    # Test Data
    JSON = 'lab/vix/sample_response/response.json'
    with open(JSON) as jsonfile:
        chain = json.loads(jsonfile.read())

        return chain
    else:
        # chain = getOptionChainTD(ticker, timeRange)
        # return chain


def collectOptionExpirations(chain):
    """
    1. Fetches all option expiration dates from IEX api. 
    2. Finds this month's expiration and next months expiration (the near-term and next-term expirations).
    3. Calculates and returns a dict containing the near-term and next-term expiration dates, along with the 
    option chain for those dates. 
    """

    # Just some simple variables we will need.
    today = datetime.datetime.now()
    year = today.year
    month = today.month
    next_month = (today + relativedelta(months=+1)).month
    next_month_year = (today + relativedelta(months=+1)).year
    next_month_end = calendar.monthrange(next_month_year, next_month)[1]

    # Our container for collecting our nearest options
    options = {
        'nearTerm': {},
        'nextTerm': {}
    }    

        """ Step 2: Finding this and next month's closest option expiration dates. """
        for optionSide in ['callExpDateMap', 'putExpDateMap']:
            if (optionSide not in options['nearTerm']):
                options['nearTerm'][optionSide] = {}
            if (optionSide not in options['nextTerm']):
                options['nextTerm'][optionSide] = {}

            for expir, strikes in chain[optionSide].items():
                expDate = datetime.datetime.strptime(expir.split(':')[0], '%Y-%m-%d')
                expMonth = expDate.month
                expYear = expDate.year

                """ Near-Term Options """
                if ((month == expMonth) and (year == expYear)):
                    firstStrike = next(iter(strikes.values()))[0]  # Just grabbing the first row of the strikes dict.
                    daysToExpiration = int(firstStrike['daysToExpiration'])
                    preciseExpiration = int(firstStrike['expirationDate'])

                    # “Near-term” options must have at least one week to expiration; a requirement
                    # intended to minimize pricing anomalies that might occur close to expiration.
                    # https://www.optionseducation.org/referencelibrary/white-papers/page-assets/vixwhite.aspx

                    if (daysToExpiration > 7):  # Must be at least 7 days from expiration.
                        options['nearTerm'][optionSide][preciseExpiration] = strikes

                """ Next-Term Options """
                if ((next_month == expMonth) and (next_month_year == expYear)):
                    firstStrike = next(iter(strikes.values()))[0]  # Just grabbing the first row of the strikes dict.
                    daysToExpiration = int(firstStrike['daysToExpiration'])
                    preciseExpiration = int(firstStrike['expirationDate'])

                    if (daysToExpiration >= 30):  # Generally around or more than 30 days to expiration.

                        options['nextTerm'][optionSide][preciseExpiration] = strikes

    """
    Step 3: Calculating the nearest option of each group of options, 
    finding min() value of each group's keys, which again, are the time to expiration in seconds.
    """

    results = {
        # Grabbing the nearest calls, will use these expirations to find associated put options.
        'nearTerm': {
            'call': options['nearTerm']['callExpDateMap'][min(options['nearTerm']['callExpDateMap'].keys())],
        },
        'nextTerm': {
            'call': options['nextTerm']['callExpDateMap'][min(options['nextTerm']['callExpDateMap'].keys())],
        },
    }

    # Finding associated put options from call expirations; making sure we have both the call and put options for the same
    # expiration date.
    for term, call in results.items():
        key = next(iter(results[term]['call'].values()))[0]['expirationDate']  # Grabbing expiration date from call
        results[term]['put'] = options[term]['putExpDateMap'][key]

    return results


def calculateForwardLevel(expirations):
    """
    "Determine the forward SPX level, F, by identifying the strike price at which the
    absolute difference between the call and put prices is smallest."
    https://www.optionseducation.org/referencelibrary/white-papers/page-assets/vixwhite.aspx

    """
    strikes = {
        'nearTerm': {},
        'nextTerm': {}
    }

    priceDiffs = {
        'nearTerm': {},
        'nextTerm': {}
    }

    # Collecting prices on call and put options with strike price as key.
    for term, options in expirations.items():
        for side, option in options.items():
            for strike, details in option.items():

                if (not strikes[term].get(strike, False)):
                    strikes[term][strike] = []
                strikes[term][strike].append(details[0]['last'])

    # Collect price differences from call and put options.
    for term, strike in strikes.items():
        for strprice, prices in strike.items():
            if (len(prices) == 2):
                p1 = prices[0]
                p2 = prices[1]

                if ((0 in [p1, p2]) == False):
                    diff = abs(p1 - p2)
                    priceDiffs[term][diff] = strprice

    # Select the smallest price difference out of the bunch.
    nearTermStrike = priceDiffs['nearTerm'][min(priceDiffs['nearTerm'].keys())]
    nextTermStrike = priceDiffs['nextTerm'][min(priceDiffs['nextTerm'].keys())]

    results = {
        'nearTerm': [
            expirations['nearTerm']['call'][nearTermStrike][0],
            expirations['nearTerm']['put'][nearTermStrike][0],
        ],
        'nextTerm': [
            expirations['nextTerm']['call'][nearTermStrike][0],
            expirations['nextTerm']['put'][nearTermStrike][0],
        ]
    }

    return results


def calculateT(strikes):
    """
    T = {MCurrent day + MSettlement day + MOther days}/ Minutes in a year 
    https://www.optionseducation.org/referencelibrary/white-papers/page-assets/vixwhite.aspx
    """

    # Near and Next-term expirations
    nearTermExpiration = strikes['nearTerm'][0]['expirationDate']
    nextTermExpiration = strikes['nextTerm'][0]['expirationDate']

    # Some variables we will need
    now = timezone('US/Central').localize(datetime.datetime.now())
    midnight = (now + datetime.timedelta(days=1)).replace(hour=0, minute=0)
    minutesToMidnight = ((midnight - now).seconds / 60)  # MCurrentDay
    mSettlementDay = 510  # minutes from midnight until 8:30 a.m. on {ticker} settlement day
    minutesYear = 525600

    # Near-Term (T1)
    expDateObj = datetime.datetime.fromtimestamp(float(nearTermExpiration / 1000))  # Windows workaround
    # The previous division by 1000 is simply a workaround for Windows. Windows doesn't seem to play nice
    # with timestamps in miliseconds.
    tzAware = timezone('US/Central').localize(expDateObj)  # Converting to timezone
    timeDiff = abs(tzAware - now)
    nrSecondsToExpire = int((timeDiff.total_seconds() // 60) - 1440)  # Calulcating time in seconds

    #Next-Term (T2)
    expDateObj = datetime.datetime.fromtimestamp(float(nextTermExpiration / 1000))  # Windows workaround
    tzAware = timezone('US/Central').localize(expDateObj)  # Converting to timezone
    timeDiff = abs(tzAware - now)
    nxtSecondsToExpire = int((timeDiff.total_seconds() // 60) - 1440)  # Calulcating time in seconds

    nrMinutesToExpire = (nrSecondsToExpire / 60)  # MOther days
    nxtMinutesToExpire = (nxtSecondsToExpire / 60)  # MOther days

    t1 = (minutesToMidnight + mSettlementDay + nrMinutesToExpire) / minutesYear
    t2 = (minutesToMidnight + mSettlementDay + nxtMinutesToExpire) / minutesYear

    return t1, t2


def calculateF(t1, t2, r, forwardLevel):
    """
    F = Strike Price + eRT × (Call Price – Put Price)
    "Determine the forward SPX level, F, by identifying the strike price at which the
    absolute difference between the call and put prices is smallest."
    https://www.optionseducation.org/referencelibrary/white-papers/page-assets/vixwhite.aspx

    """


    strikePrice = forwardLevel['nearTerm'][0]['strikePrice']

    # Near-Term    
    callPrice = forwardLevel['nearTerm'][0]['last']
    putPrice = forwardLevel['nearTerm'][1]['last']
    
    f1 = strikePrice + e**(r*t1) * (callPrice - putPrice)

    # Next-Term
    callPrice = forwardLevel['nextTerm'][0]['last']
    putPrice = forwardLevel['nextTerm'][1]['last']
    
    f2 = strikePrice + e**(r*t2) * (callPrice - putPrice)
    
    return f1, f2


def calcaulateK():
    """
    """


def deltaK():
    """
    """




#
# for later
# The following division by 1000 is simply a workaround for Windows. Windows doesn't seem to play nice
# with timestamps in miliseconds.

# expirationObj = datetime.datetime.fromtimestamp(float(preciseExpiration / 1000))  # Windows workaround
# timeDiff = abs(expirationObj - today)
# secondsToExpiration = int((timeDiff.total_seconds() // 60) - 1440)  # Calulcating time in seconds

# options['nextTerm'][optionSide][preciseExpiration] = {
#     'daysToExpiration': daysToExpiration,
#     'secondsToExpiration': secondsToExpiration,
#     'preciseExpiration': preciseExpiration,
#     'chain': strikes,
# }
