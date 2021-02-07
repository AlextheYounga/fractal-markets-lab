import json
import sys
import datetime
import time
import calendar
from pytz import timezone
from dateutil.relativedelta import relativedelta
from ..core.api.options import *
import pandas as pd
import numpy as np
import calendar


def calculateT():
    """
    Step 2 of VIX equation
    """

def collectOptionExpirations(ticker, testing=False):
    """
    Step 1 of VIX equation.
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

    # Building a timerange to send to TD Ameritrade's API
    fromDate = today
    toDate = datetime.datetime(next_month_year, next_month, next_month_end)
    timeRange = [fromDate, toDate]

    """ Step 1: Fetch the option chain from TD Ameritrade """
    # chain = getOptionChainTD(ticker, timeRange, 'OTM')

    # Testing purposes
    JSON = 'lab/vix/optionData/response.json'
    with open(JSON) as jsonfile:
        chain = json.loads(jsonfile.read())

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
                    firstStrike = next(iter(strikes.values()))[0] #Just grabbing the first row of the strikes dict.
                    daysToExpiration = int(firstStrike['daysToExpiration'])
                    preciseExpiration = int(firstStrike['expirationDate'])

                    # “Near-term” options must have at least one week to expiration; a requirement
                    # intended to minimize pricing anomalies that might occur close to expiration.
                    # https://www.optionseducation.org/referencelibrary/white-papers/page-assets/vixwhite.aspx

                    if (daysToExpiration > 7):  # Must be at least 7 days from expiration.

                        # The following division by 1000 is simply a workaround for Windows. Windows doesn't seem to play nice
                        # with timestamps in miliseconds.

                        expirationObj = datetime.datetime.fromtimestamp(float(preciseExpiration / 1000))  # Windows workaround
                        timeDiff = abs(expirationObj - today)
                        secondsToExpiration = int((timeDiff.total_seconds() // 60) - 1440)  # Calulcating time in seconds

                        options['nearTerm'][optionSide][preciseExpiration] = {
                            'daysToExpiration': daysToExpiration,
                            'secondsToExpiration': secondsToExpiration,
                            'preciseExpiration': preciseExpiration,
                            'chain': strikes,
                        }

                """ Next-Term Options """
                if ((next_month == expMonth) and (next_month_year == expYear)):
                    firstStrike = next(iter(strikes.values()))[0] #Just grabbing the first row of the strikes dict.
                    daysToExpiration = int(firstStrike['daysToExpiration'])
                    preciseExpiration = int(firstStrike['expirationDate'])

                    if (daysToExpiration >= 30):  # Generally around or more than 30 days to expiration.

                        expirationObj = datetime.datetime.fromtimestamp(float(preciseExpiration / 1000))  # Windows workaround
                        timeDiff = abs(expirationObj - today)
                        secondsToExpiration = int((timeDiff.total_seconds() // 60) - 1440)  # Calulcating time in seconds

                        options['nextTerm'][optionSide][preciseExpiration] = {
                            'daysToExpiration': daysToExpiration,
                            'secondsToExpiration': secondsToExpiration,
                            'preciseExpiration': preciseExpiration,
                            'chain': strikes,
                        }

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
        key = results[term]['call']['preciseExpiration']
        results[term]['put'] = options[term]['putExpDateMap'][key]

    return results


def calculateF(expirations):
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

    results = {
        'nearTerm': {},
        'nextTerm': {}
    }

    # Collecting prices on call and put options with strike price as key.
    for term, options in expirations.items():
        for side, option in options.items():
            for strike, details in option['chain'].items():
                # print(side+' - '+strike)
                if (not strikes[term].get(strike, False)):
                    strikes[term][strike] = []
                strikes[term][strike].append(details[0]['last'])


    # Collect price differnces from call and put options. 
    for term, strike in strikes.items():
        for strprice, prices in strike.items():
            if (len(prices) == 2):
                p1 = prices[0]
                p2 = prices[1]

                if ((0 in [p1, p2]) == False):
                    diff = abs(p1 - p2)
                    priceDiffs[term][diff] = strprice

    # Select the smallest price difference out of the bunch.
    f1 = 
    
    print(json.dumps(priceDiffs, indent=1))
    sys.exit()

    # print(json.dumps(strikes, indent=1))
    # sys.exit()

    # for term in [nearTermExpir, nextTermExpir]:
    #     chain = getOptionChain(ticker, term, sandbox)
