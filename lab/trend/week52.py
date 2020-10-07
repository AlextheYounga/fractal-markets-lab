import statistics
import json
import os
import sys
from .functions import *
from ..shared.functions import *
from ..shared.api import getCurrentPrice
from ..shared.output import printTable
from ..shared.imports import parseCSV
from ..shared.export import writeCSV
import texttable
from dotenv import load_dotenv
import requests
load_dotenv()

nasdaq = parseCSV('NasdaqComposite.csv')

# print(json.dumps(nasdaq, indent=1))


def getTrendData(ticker):
    price = getCurrentPrice(ticker)

    url = 'https://cloud.iexapis.com/stable/stock/{}/stats?token={}'.format(ticker, os.environ.get("IEX_TOKEN"))
    stats = requests.get(url).json()

    return price, stats


results = {}
for i, stock in nasdaq.items():
    price, stats = getTrendData(stock['ticker'])

    week52high = stats['week52high'] if 'week52high' in stats else 0
    fromHigh = round((price / week52high) * 100, 3)
    eps = stats['ttmEPS'] if 'ttmEPS' in stats else 0

    if ((fromHigh < 110) and (fromHigh > 95)):
        if (eps > 0):
            if (stats['day5ChangePercent'] > 10):
                print(stock['ticker'] + "\n")
                keyStats = {
                    'week52high': stats['week52high'],
                    'ttmEPS': stats['ttmEPS'],
                    'peRatio': stats['peRatio'],
                    'day5ChangePercent': stats['day5ChangePercent'],
                    'month1ChangePercent': stats['month1ChangePercent'],
                    'day50MovingAvg': stats['day50MovingAvg'],
                    'day200MovingAvg': stats['day200MovingAvg'],
                }
                data = {stock, keyStats}
                data['price'] = price
                results[i] = data
    else:
        print('.', end="")
        sys.stdout.flush()

for item in results.items():
    printTable(item)

writeCSV(results, 'trend/trend_chasing.csv')
