from ..key import IEX_TOKEN
from iexfinance.stocks import get_historical_data
import json
import csv
from datetime import datetime, timedelta


def getShortApiData(asset):
    start = datetime.today() - timedelta(days=30)
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

def getLongApiData(asset):
    start = datetime(2016, 1, 1)
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
