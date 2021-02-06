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


def calculateOptionExpirations(ticker, testing=False):
    """
    1. Fetches all option expiration dates from IEX api. 
    2. Finds this month's expiration and next months expiration (the near-term and next-term expirations).
    3. Calculates and returns a dict containing the near-term and next-term expiration dates, along with the 
    option chain for those dates. 
    """

    today = datetime.datetime.now()
    # "...and reflect prices observed at the open of trading – 8:30 a.m. Chicago time."
    # https://www.optionseducation.org/referencelibrary/white-papers/page-assets/vixwhite.aspx

    # Just some simple variables we will need.
    year = today.year
    month = today.month
    next_month = (today + relativedelta(months=+1)).month
    next_month_year = (today + relativedelta(months=+1)).year
    next_month_end = calendar.monthrange(next_month_year, next_month)[1]
    near_term_options = {}
    next_term_options = {}

    # Building a timerange to send to TD Ameritrade's API
    fromDate = today
    toDate = datetime.datetime(next_month_year, next_month, next_month_end)
    timeRange = [fromDate, toDate]

    # Step 1: Fetch the chain from TD Ameritrade
    # chain = getOptionChainTD(ticker, timeRange, 'OTM')

    # Testing purposes
    JSON = 'lab/vix/optionData/response.json'
    with open(JSON) as jsonfile:
        chain = json.loads(jsonfile.read())
        for optionSide in ['callExpDateMap', 'putExpDateMap']:
            for expir, strikes in chain[optionSide].items():
                expDate = datetime.datetime.strptime(expir.split(':')[0], '%Y-%m-%d')
                expMonth = expDate.month
                expYear = expDate.year

                if ((month == expMonth) and (year == expYear)):                    
                    firstStrike = next(iter(strikes.values()))[0]
                    daysToExpiration = int(firstStrike['daysToExpiration'])
                    preciseExpiration = int(firstStrike['expirationDate'])

                    # “Near-term” options must have at least one week to expiration; a requirement
                    # intended to minimize pricing anomalies that might occur close to expiration.
                    # https://www.optionseducation.org/referencelibrary/white-papers/page-assets/vixwhite.aspx

                    if (daysToExpiration > 7): # Must be at least 7 days from expiration.

                        # The following division by 1000 is simply a workaround for Windows. Windows doesn't seem to play nice 
                        # with timestamps in miliseconds. 

                        expirationObj = datetime.datetime.fromtimestamp(float(preciseExpiration / 1000)) #Windows workaround
                        timeDiff = abs(expirationObj - today)
                        secondsToExpiration = int((timeDiff.total_seconds() // 60) - 1440) #Calulcating time in seconds

                        near_term_options[preciseExpiration] = {
                            'daysToExpiration': daysToExpiration,
                            'secondsToExpiration': secondsToExpiration,
                            'preciseExpiration': preciseExpiration,
                            'chain': strikes,
                        }

                if ((next_month == expMonth) and (next_month_year == expYear)):                    
                    firstStrike = next(iter(strikes.values()))[0]
                    daysToExpiration = int(firstStrike['daysToExpiration'])
                    preciseExpiration = int(firstStrike['expirationDate'])

                    if (daysToExpiration >= 30): # Generally around or more than 30 days to expiration.

                        expirationObj = datetime.datetime.fromtimestamp(float(preciseExpiration / 1000)) #Windows workaround
                        timeDiff = abs(expirationObj - today)
                        secondsToExpiration = int((timeDiff.total_seconds() // 60) - 1440) #Calulcating time in seconds

                        next_term_options[preciseExpiration] = {
                            'daysToExpiration': daysToExpiration,
                            'secondsToExpiration': secondsToExpiration,
                            'preciseExpiration': preciseExpiration,
                            'chain': strikes,
                        }
    
    results = {
        'nearTerm': near_term_options[min(near_term_options.keys())],
        'nextTerm': next_term_options[min(next_term_options.keys())],
    }

    return results


def calculateF(ticker, expirations, sandbox=False):
    """
    Test
    """
    nearTermExpir = expirations['nearTerm']['expirationDate']
    nextTermExpir = expirations['nextTerm']['expirationDate']
    print(nearTermExpir)

    chain = getOptionChain(ticker, nearTermExpir, sandbox)
    print(chain)
    sys.exit()

    # for term in [nearTermExpir, nextTermExpir]:
    #     chain = getOptionChain(ticker, term, sandbox)
