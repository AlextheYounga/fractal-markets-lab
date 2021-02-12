from dotenv import load_dotenv
import requests
import sys
import json
import os
load_dotenv()

def syncStocks():
    """
    Fetches all stocks from IEX 

    Returns
    -------
    object of all stocks 
    """
    try:
        url = 'https://cloud.iexapis.com/stable/ref-data/iex/symbols?token={}'.format(os.environ.get("IEX_TOKEN"))
        tickers = requests.get(url).json()
    except:
        #print("Unexpected error:", sys.exc_info()[0])
        return {}

    return tickers