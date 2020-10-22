import django
from django.apps import apps
import statistics
import json
import os
import sys
from datetime import datetime
from datetime import date
from .functions import *
from ..shared.functions import *
from ..shared.api import getCurrentPrice
from ..shared.output import printTable
from ..shared.export import writeCSV
import texttable
from dotenv import load_dotenv
import requests
load_dotenv()
django.setup()


Stock = apps.get_model('database', 'Stock')
stocks = Stock.objects.order_by('ticker').values('ticker').distinct()

# print(json.dumps(nasdaq, indent=1))


def getTrendData(ticker):
    try:
        price = getCurrentPrice(ticker)
        url = 'https://cloud.iexapis.com/stable/stock/{}/stats?token={}'.format(ticker, os.environ.get("IEX_TOKEN"))
        stats = requests.get(url).json()

        return price, stats
    except:
        return None, None


def checkEarnings(ticker):
    url = 'https://cloud.iexapis.com/stable/stock/{}/earnings?token={}'.format(ticker, os.environ.get("IEX_TOKEN"))
    earnings = requests.get(url).json()

    return earnings


print('Running...')
results = []
for stock in stocks:
    print(stock.ticker)
    sys.exit()
    price, stats = getTrendData(stock.ticker)

    if (price == None or stats == None):
        continue

    week52high = stats['week52high'] if 'week52high' in stats else 0
    if (week52high == 0 or week52high == None):
        continue

    fromHigh = round((price / week52high) * 100, 3)
    eps = stats['ttmEPS'] if 'ttmEPS' in stats else 0
    if (eps == 0 or eps == None):
        continue

    if (stats['day5ChangePercent'] == None or stats['day5ChangePercent'] == 0):
        continue
    day5ChangePercent = stats['day5ChangePercent'] * 100

    if ((fromHigh < 110) and (fromHigh > 90)):
        if (eps > 0):
            if (day5ChangePercent > 10):
                earningsData = checkEarnings(stock['ticker'])
                earnings = earningsData['earnings']

                keyStats = {
                    'week52high': stats['week52high'],
                    'ttmEPS': stats['ttmEPS'],
                    'lastEPS': earnings['actualEPS'] if 'actualEPS' in earnings else 'NA',
                    'consensus': earnings['consensusEPS'] if 'consensusEPS' in earnings else 'NA',
                    'surprise': earnings['EPSSurpriseDollar']  if 'EPSSurpriseDollar' in earnings else 'NA',
                    'yearAgoEPS': earnings['yearAgo']  if 'yearAgo' in earnings else 'NA',
                    'peRatio': stats['peRatio'],
                    'day5ChangePercent': stats['day5ChangePercent'],
                    'month1ChangePercent': stats['month1ChangePercent'],
                    'day50MovingAvg': stats['day50MovingAvg'],
                    'day200MovingAvg': stats['day200MovingAvg'],
                    'fromHigh': fromHigh,
                }

                stock.update(keyStats)
                stock['price'] = price
                results.append(stock)
                printTable(stock)

if results:
    today = date.today().strftime('%m-%d')
    writeCSV(results, 'trend/trend_chasing_{}.csv'.format(today))
