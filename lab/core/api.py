from iexfinance.stocks import get_historical_data
from iexfinance.stocks import Stock
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests
import json
import csv
import os
load_dotenv()


def syncStocks():
    try:
        url = 'https://cloud.iexapis.com/stable/ref-data/iex/symbols?token={}'.format(os.environ.get("IEX_TOKEN"))
        tickers = requests.get(url).json()
    except:
        return {}

    return tickers


def quoteStatsBatchRequest(batch):
    # Accepts list of tickers
    # Maximum 100   
    
    batch = ",".join(batch)  # Convert to comma-separated string
    try:
        url = 'https://cloud.iexapis.com/stable/stock/market/batch?symbols={}&types=quote,stats&token={}'.format(batch, os.environ.get("IEX_TOKEN"))
        batch_request = requests.get(url).json()
    except:
        return {}

    return batch_request


def companyBatchRequest(batch):
    # Accepts list of tickers
    # Maximum 100
    try:
        batch = ",".join(batch)  # Convert to comma-separated string
        url = 'https://cloud.iexapis.com/stable/stock/market/batch?symbols={}&types=quote,company&token={}'.format(batch, os.environ.get("IEX_TOKEN"))
        batch_request = requests.get(url).json()
    except:
        return {}

    return batch_request


def getCurrentPrice(ticker):
    try:
        stock = Stock(ticker, token=os.environ.get("IEX_TOKEN"))
        price = stock.get_price()
    except:
        return {}

    return price


def getStockInfo(ticker):
    try:
        stock = Stock(ticker, token=os.environ.get("IEX_TOKEN"))
        company = stock.get_company()
    except:
        return {}

    return company


def getCustomTimeRange(ticker, time):
    try:
        start = datetime.today() - timedelta(days=time)
        end = datetime.today()

        api_response = get_historical_data(ticker, start, end, token=os.environ.get("IEX_TOKEN"))
        asset_data = {}
        i = 0
        for day, quote in api_response.items():
            asset_data[i] = {
                'date': day,
                'open': quote['open'],
                'close': quote['close'],
                'high': quote['high'],
                'low': quote['low'],
                'volume': quote['volume']
            }
            i = i + 1
    except:
        return {}

    return asset_data


def getShortTermData(ticker):
    try:
        start = datetime.today() - timedelta(days=64)
        end = datetime.today()

        api_response = get_historical_data(ticker, start, end, token=os.environ.get("IEX_TOKEN"))
        asset_data = {}
        i = 0
        for day, quote in api_response.items():
            asset_data[i] = {
                'date': day,
                'open': quote['open'],
                'close': quote['close'],
                'high': quote['high'],
                'low': quote['low'],
                'volume': quote['volume']
            }
            i = i + 1

    except:
        return {}

    return asset_data


def getShortTermPrices(ticker):
    try:
        start = datetime.today() - timedelta(days=64)
        end = datetime.today()

        api_response = get_historical_data(ticker, start, end, close_only=True, token=os.environ.get("IEX_TOKEN"))
        asset_data = {}
        i = 0
        for day, quote in api_response.items():
            asset_data[i] = {
                'date': day,
                'close': quote['close'],
                'volume': quote['volume']
            }
            i = i + 1

    except:
        return {}

    return asset_data


def getLongTermPrices(ticker):
    """ BEWARE, VERY HIGH MESSAGE USE! """
    try:
        url = 'https://cloud.iexapis.com//stable/stock/{}/chart/2y?token={}'.format(ticker, param, os.environ.get("IEX_TOKEN"))
        api_response = requests.get(url).json()
        asset_data = {}

        for i, day in enumerate(api_response):
            asset_data[i] = {
                'date': day['date'],
                'close': day['close'],
                'open': day['open'],
                'high': day['high'],
                'low': day['low'],
                'volume': day['volume']
            }

    except:
        return {}

    return asset_data


def getLongTermPrices(ticker):
    try:
        param = 'chartCloseOnly=true'
        url = 'https://cloud.iexapis.com/stable/stock/{}/chart/2y?{}&token={}'.format(ticker, param, os.environ.get("IEX_TOKEN"))
        api_response = requests.get(url).json()
        asset_data = {}

        for i, day in enumerate(api_response):
            asset_data[i] = {
                'date': day['date'],
                'close': day['close'],
                'volume': day['volume']
            }

    except:
        return {}

    return asset_data


def getQuoteData(ticker):
    try:
        stock = Stock(ticker, token=os.environ.get("IEX_TOKEN"))
        quote = stock.get_quote()
    except:
        return {}

    return quote


# ----------------------------------------------
# Testing Queries using IEX Sandbox
# ----------------------------------------------
def testShortTermPrices(ticker):
    try:
        # Set IEX Finance API Token (Test)
        os.environ['IEX_API_VERSION'] = 'iexcloud-sandbox'
        start = datetime.today() - timedelta(days=64)
        end = datetime.today()

        api_response = get_historical_data(ticker, start, end, token=os.environ.get("IEX_SANDBOX_TOKEN"))
        asset_data = {}
        i = 0
        for day, quote in api_response.items():
            asset_data[i] = {
                'date': day,
                'open': quote['open'],
                'close': quote['close'],
                'high': quote['high'],
                'low': quote['low'],
                'volume': quote['volume']
            }
            i = i + 1
        os.environ['IEX_API_VERSION'] = 'v1'

    except:
        return {}

    return asset_data


def testLongTermPrices(ticker):
    try:
        param = 'chartCloseOnly=true'
        url = 'https://sandbox.iexapis.com/stable/stock/{}/chart/2y?{}&token={}'.format(ticker, param, os.environ.get("IEX_SANDBOX_TOKEN"))
        api_response = requests.get(url).json()
        asset_data = {}

        for i, day in enumerate(api_response):
            asset_data[i] = {
                'date': day['date'],
                'close': day['close'],
                'volume': day['volume']
            }

    except:
        return {}

    return asset_data
