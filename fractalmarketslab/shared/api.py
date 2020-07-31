from ..key import *
from iexfinance.stocks import get_historical_data
from iexfinance.stocks import Stock
import json
import csv
from datetime import datetime, timedelta
import os


def getCustomTimeRange(asset, time):
    start = datetime.today() - timedelta(days=time)
    end = datetime.today()

    api_response = get_historical_data(asset, start, end, token=IEX_TOKEN)
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


def getShortTermPrices(asset):
    start = datetime.today() - timedelta(days=10)
    end = datetime.today()

    api_response = get_historical_data(asset, start, end, token=IEX_TOKEN)
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


def testShortTermPrices(asset):
    # Set IEX Finance API Token (Test)
    os.environ['IEX_API_VERSION'] = 'iexcloud-sandbox'
    start = datetime.today() - timedelta(days=30)
    end = datetime.today()

    api_response = get_historical_data(asset, start, end, token=IEX_SANDBOX_TOKEN)
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

def getLongTermData(asset):
    start = datetime.today() - timedelta(days=100)
    end = datetime.today()

    api_response = get_historical_data(asset, start, end, token=IEX_TOKEN)
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


def getLongTermPrices(asset):
    start = datetime.today() - timedelta(days=100)
    end = datetime.today()

    api_response = get_historical_data(asset, start, end, close_only=True, token=IEX_TOKEN)
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


def getCurrentPrice(asset):
    stock = Stock(asset, token=IEX_TOKEN)
    price = stock.get_price()

    return price
