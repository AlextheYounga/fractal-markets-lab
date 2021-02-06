from datetime import datetime, time, timedelta
from dotenv import load_dotenv
import requests
import sys
import json
import os
load_dotenv()


def getExpirations(ticker, sandbox=False):
    """
    Fetches all options expiration dates from a ticker

    Parameters
    ----------
    ticker      :string
    sandbox     :bool
                Sets the IEX environment to sandbox mode to make limitless API calls for testing.

    Returns
    -------
    list of option expiration dates
    """
    domain = 'cloud.iexapis.com'
    key = os.environ.get("IEX_TOKEN")
    if (sandbox):
        domain = 'sandbox.iexapis.com'
        key = os.environ.get("IEX_SANDBOX_TOKEN")
    try:
        url = 'https://{}/stable/stock/{}/options?token={}'.format(
            domain,
            ticker,
            key
        )
        options = requests.get(url).json()
    except:
        #print("Unexpected error:", sys.exc_info()[0])
        return None

    return options


def getOptionChain(ticker, date, sandbox=False):
    """
    Fetches the option chain (calls and puts), for a ticker.

    Parameters
    ----------
    ticker      :string
    date        :datetime.datetime
    sandbox     :bool
                Sets the IEX environment to sandbox mode to make limitless API calls for testing.

    Returns
    -------
    list of option expiration dates
    """
    def formatDate(date):
        if (type(date) == 'datetime.datetime'):
            fdate = datetime.strftime(date, '%Y%m%d')
            return fdate
        else:
            print('Failure in getOptionChain(). Date param must be of type datetime.datetime. Closing program...')
            sys.exit()

    fdate = formatDate(date)
    domain = 'cloud.iexapis.com'
    key = os.environ.get("IEX_TOKEN")

    if (sandbox):
        domain = 'sandbox.iexapis.com'
        key = os.environ.get("IEX_SANDBOX_TOKEN")
            
    try:
        url = 'https://{}/stable/stock/{}/options/{}?token={}'.format(
            domain,
            ticker,
            fdate,
            key
        )
        chain = requests.get(url).json()
    except:
        #print("Unexpected error:", sys.exc_info()[0])
        return None

    return chain

