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
