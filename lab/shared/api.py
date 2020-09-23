from iexfinance.stocks import get_historical_data
from iexfinance.stocks import Stock
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests
import json
import csv
import os
load_dotenv()


def getCustomTimeRange(ticker, time):
    start = datetime.today() - timedelta(days=time)
    end = datetime.today()

    api_response = get_historical_data(ticker, start, end, token=os.environ.get("IEX_TOKEN"))
    # api_response = get_historical_data(ticker, 2yr, token=os.environ.get("IEX_TOKEN"))
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

    return asset_data


def getShortTermData(ticker):
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

    return asset_data


def getShortTermPrices(ticker):
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

    return asset_data


# BEWARE, VERY HIGH MESSAGE USE!
def getLongTermPrices(ticker):
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

    return asset_data


def getLongTermPrices(ticker):
    param = 'chartCloseOnly=true'
    url = 'https://cloud.iexapis.com//stable/stock/{}/chart/2y?{}&token={}'.format(ticker, param, os.environ.get("IEX_TOKEN"))
    api_response = requests.get(url).json()
    asset_data = {}

    for i, day in enumerate(api_response):
        asset_data[i] = {
            'date': day['date'],
            'close': day['close'],
            'volume': day['volume']
        }

    return asset_data


def getCurrentPrice(ticker):
    stock = Stock(ticker, token=os.environ.get("IEX_TOKEN"))
    price = stock.get_price()

    return price

def getQuoteData():
    return


def testShortTermPrices(ticker):
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

    return asset_data


def testLongTermPrices(ticker):
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

    return asset_data



