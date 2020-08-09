# from ..key import *
from iexfinance.stocks import get_historical_data
from iexfinance.stocks import Stock
import requests
import json
import csv
from datetime import datetime, timedelta
import os


def getCustomTimeRange(ticker, time):
    start = datetime.today() - timedelta(days=time)
    end = datetime.today()

    api_response = get_historical_data(ticker, start, end, token=os.environ['IEX_TOKEN'])
    # api_response = get_historical_data(ticker, 2yr, token=os.environ['IEX_TOKEN'])
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
    start = datetime.today() - timedelta(days=30)
    end = datetime.today()

    api_response = get_historical_data(ticker, start, end, token=os.environ['IEX_TOKEN'])
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
    start = datetime.today() - timedelta(days=30)
    end = datetime.today()

    api_response = get_historical_data(ticker, start, end, close_only=True, token=os.environ['IEX_TOKEN'])
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
def getLongTermData(ticker):
    start = datetime.today() - timedelta(days=100)
    end = datetime.today()

    api_response = get_historical_data(ticker, start, end, token=os.environ['IEX_TOKEN'])
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


def getLongTermPrices(ticker):
    start = datetime.today() - timedelta(days=100)
    end = datetime.today()

    api_response = get_historical_data(ticker, start, end, close_only=True, token=os.environ['IEX_TOKEN'])
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


def getCurrentPrice(ticker):
    stock = Stock(ticker, token=os.environ['IEX_TOKEN'])
    price = stock.get_price()

    return price


def testShortTermPrices(ticker):
    # Set IEX Finance API Token (Test)
    os.environ['IEX_API_VERSION'] = 'iexcloud-sandbox'
    start = datetime.today() - timedelta(days=30)
    end = datetime.today()

    api_response = get_historical_data(ticker, start, end, token=os.environ['IEX_SANDBOX_TOKEN'])
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
    api_call =requests.get('https://sandbox.iexapis.com/stable/stock/{}/chart/2y?token={}'.format(ticker, os.environ['IEX_SANDBOX_TOKEN']))

    api_response = get_historical_data(ticker, start, end, token=os.environ['IEX_SANDBOX_TOKEN'])
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


def parseCSV(file):
    with open('fractalmarketslab/imports/{}'.format(file), newline='', encoding='utf-8') as csvfile:
        asset_data = {}
        reader = csv.DictReader(csvfile)

        for i, row in enumerate(reader):
            # Using powers of 2
            rows = {
                'date': row['\ufeffDate'] if row['\ufeffDate'] else '',
                'close': row['Close'] if row['Close'] else 0
            }
            # Append value dictionary to data
            asset_data[i] = rows
    return asset_data
