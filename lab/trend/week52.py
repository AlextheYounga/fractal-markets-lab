import statistics
import json
import os
import sys
from .functions import *
from ..shared.functions import *
from ..shared.imports import parseCSV
from tabulate import tabulate
from dotenv import load_dotenv
import requests
load_dotenv()

nasdaq = parseCSV('NasdaqComposite.csv')

# print(json.dumps(nasdaq, indent=1))

def getTrendData(ticker):
    param = 'latestPrice,week52High,changePercent,ytdChange,peRatio'
    url = 'https://cloud.iexapis.com//stable/stock/{}/quote?filter={}&token={}'.format(ticker, param, os.environ.get("IEX_TOKEN"))
    trend = requests.get(url).json()

    url = 'https://cloud.iexapis.com//stable/stock/{}/stats?token={}'.format(ticker, param, os.environ.get("IEX_TOKEN"))
    stats = requests.get(url).json()

    return trend, stats

promising = {}
for i, stock in nasdaq.items():
    trendData, earningsData = getTrendData(stock['ticker'])
    earnings = earningsData['earnings'] if 'earnings' in earningsData else None
    if earnings == None:
     continue
    # Trend
    week52high = trendData['week52High'] if 'week52High' in trendData else 0
    price = trendData['latestPrice'] if 'latestPrice' in trendData else 0
    changePercent = trendData['changePercent'] if 'changePercent' in trendData else 0
    fromHigh = round((price / week52high) * 100, 3)
    # Earnings
    eps = earnings['actualEPS'] if 'actualEPS' in earnings else 0
    epsChange = earnings['yearAgoChangePercent'] if 'yearAgoChangePercent' in earnings else 0
    print(eps)
    if ((fromHigh < 110) and (fromHigh > 95)):

        if ((eps > 0) and (epsChange > 0)):

            if (changePercent > 3):
                print(stock['ticker'])       
                data = {stock, trendData, earnings}
                promising[i] = data
    else:
        print('.', end = "")
        sys.stdout.flush()
    

print(json.dumps(promising, indent=1))