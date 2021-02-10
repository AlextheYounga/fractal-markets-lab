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
    else:
        chain = getOptionChainTD()
    return chain


def selectOptionExpirations(chain):
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

    selectedChain = {
        # Grabbing the nearest calls, will use these expirations to find associated put options.
        'nearTerm': {
            'call': options['nearTerm']['callExpDateMap'][min(options['nearTerm']['callExpDateMap'].keys())],
        },
        'nextTerm': {
            'call': options['nextTerm']['callExpDateMap'][min(options['nextTerm']['callExpDateMap'].keys())],
        },
    }

    selectedDates = {
        # Creating a separate dict to store some crucial date variables.
        'nearTerm': {
            'preciseExpiration': next(iter(selectedChain['nearTerm']['call'].values()))[0]['expirationDate'],
        },
        'nextTerm': {
            'preciseExpiration': next(iter(selectedChain['nextTerm']['call'].values()))[0]['expirationDate']
        }
    }

    # Date manipulation, doing here because we'll need these later.
    for term, d in selectedDates.items():
        t = d['preciseExpiration']
        dateT = datetime.datetime.fromtimestamp(float(t / 1000))  # Windows workaround
        # The previous division by 1000 is simply a workaround for Windows. Windows doesn't seem to play nice
        # with timestamps in miliseconds.
        dateObj = timezone('US/Central').localize(dateT)  # Converting to timezone
        dateStr = dateObj.strftime('%Y-%m-%d')

        selectedDates[term]['dateObj'] = dateObj
        selectedDates[term]['dateStr'] = dateStr

    # Finding associated put options from call expirations; making sure we have both the call and put options for the same
    # expiration date.
    for term, call in selectedChain.items():
        key = next(iter(selectedChain[term]['call'].values()))[0]['expirationDate']  # Grabbing expiration date from call
        selectedChain[term]['put'] = options[term]['putExpDateMap'][key]

    return selectedDates, selectedChain


def calculateForwardLevel(selectedChain):
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
    for term, options in selectedChain.items():
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
            selectedChain['nearTerm']['call'][nearTermStrike][0],
            selectedChain['nearTerm']['put'][nearTermStrike][0],
        ],
        'nextTerm': [
            selectedChain['nextTerm']['call'][nextTermStrike][0],
            selectedChain['nextTerm']['put'][nextTermStrike][0],
        ]
    }

    return results


def calculateT(selectedDates):
    """
    T = {MCurrent day + MSettlement day + MOther days}/ Minutes in a year 
    https://www.optionseducation.org/referencelibrary/white-papers/page-assets/vixwhite.aspx
    """

    # Some variables we will need
    now = timezone('US/Central').localize(datetime.datetime.now())
    midnight = (now + datetime.timedelta(days=1)).replace(hour=0, minute=0)
    minutesToMidnight = ((midnight - now).seconds / 60)  # MCurrentDay
    mSettlementDay = 510  # minutes from midnight until 8:30 a.m. on {ticker} settlement day
    minutesYear = 525600

    t = {}

    for term, date in selectedDates.items():
        timeDiff = abs(date['dateObj'] - now)
        secondsToExpire = int((timeDiff.total_seconds() // 60) - 1440)  # Calulcating time in seconds
        minutesToExpire = (secondsToExpire / 60)  # MOther days
        t[term] = (minutesToMidnight + mSettlementDay + minutesToExpire) / minutesYear  # T equation

    return t


def calculateF(t, r, forwardLevel):
    """
    F = Strike Price + eRT × (Call Price – Put Price)
    "Determine the forward SPX level, F, by identifying the strike price at which the
    absolute difference between the call and put prices is smallest."
    https://www.optionseducation.org/referencelibrary/white-papers/page-assets/vixwhite.aspx

    """
    f = {}

    strikePrice = forwardLevel['nearTerm'][0]['strikePrice']

    for term in ['nearTerm', 'nextTerm']:
        callPrice = forwardLevel[term][0]['last']
        putPrice = forwardLevel[term][1]['last']
        f[term] = strikePrice + e**(r*t[term]) * (callPrice - putPrice) # F equation

    return f


def calculateK(f, selectedChain):
    """
    """
    k = {
        'nearTerm': {},
        'nextTerm': {}
    }

    for term, options in selectedChain.items():
        bets = {}
        for side, option in options.items():
            bets[side] = {}
            for strike, details in option.items():

                # Collecting bids and asks to be used in determining 'ki'
                bid = details[0]['bid']
                ask = details[0]['ask']
                bets[side][strike] = {
                    'bid': bid,
                    'ask': ask,
                    'midquote': (bid + ask) / 2 
                }

                # Collecting k0
                # The first strike below the forward index level, F
                minFwdLvl = float(int(f[term]))
                if (float(strike) <= minFwdLvl):
                    k0 = strike
                    k[term]['k0'] = k0


        # Collecting put/call averages
        # "Finally, select both the put and call with strike price K0.
        # The following table contains the options used to calculate the VIX in this example. VIX
        # uses the average of quoted bid and ask, or mid-quote, prices for each option selected. The
        # K0 put and call prices are averaged to produce a single value."
        callMQ = bets['call'][k0]['midquote']
        putMQ = bets['put'][k0]['midquote']
        k[term]['putCallAvg'] = (callMQ + putMQ) / 2


        # Finding upper and lower boundaries on chain
        # "Select out-of-the-money put options with strike prices < K0. Start with the put
        # strike immediately lower than K0 and move to successively lower strike prices.
        # Exclude any put option that has a bid price equal to zero (i.e., no bid). As shown
        # below, once two puts with consecutive strike prices are found to have zero bid
        # prices, no puts with lower strikes are considered for inclusion."

        k[term]['bounds'] = {}
        for side, strks in bets.items():
            zeros = 0
            strklist = strks.keys()
            if (side == 'put'):
                strklist = list(reversed(strks.keys()))
            for price in strklist:

                if ((side == 'put') and (price > k[term]['k0'])): #Excluding all put prices above k0
                    continue
                if ((side == 'call') and (price < k[term]['k0'])): #Ecluding all call prices below k0
                    continue

                if (zeros == 2): #If two zero bids are encountered in a row, our answer will be the last ki set.
                    break

                b = bets[side][price]['bid']
                a = bets[side][price]['ask']

                if (b and a):
                    k[term]['bounds'][side] = price
                else:
                    zeros += 1

    return k


def calculateDeltaK(k, t, r, selectedChain):
    """
    """
    curatedStrikes = []
    contributions = {
        'nearTerm': [],
        'nextTerm': [] 
    }
    # Calculate the contribution of each call/put within the bounds.
    for term, options in selectedChain.items():
        # Created list of strikes within boundaries.  
        for side, option in options.items():
            for strike, details in option.items():
                if (side == 'call'):
                    if ((strike < k[term]['k0']) or (strike > k[term]['bounds']['call'])):
                        continue
                if (side == 'put'):
                    if ((strike > k[term]['k0']) or (strike < k[term]['bounds']['put'])):
                        continue
                curatedStrikes.append(strike)
    
    for i, price in enumerate(curatedStrikes):
        if (i == 0):
            deltaK = curatedStrikes[i + 1] - price
            contribution = 
            continue


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
