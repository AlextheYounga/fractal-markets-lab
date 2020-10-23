import django
from django.apps import apps
import statistics
import json
import os
import sys
from datetime import datetime
from datetime import date
from .functions import *
from ..database.functions import uniqueField
from ..shared.functions import *
from ..shared.api import getCurrentPrice
from ..shared.output import printTable
from ..shared.export import writeCSV
import texttable
from dotenv import load_dotenv
import requests
load_dotenv()
django.setup()


stocks = uniqueField('Stock', 'database_stock', 'ticker')


def getTrendData(ticker):
    try:
        price = getCurrentPrice(ticker)
        url = 'https://cloud.iexapis.com/stable/stock/{}/stats?token={}'.format(ticker, os.environ.get("IEX_TOKEN"))
        stats = requests.get(url).json()

        return price, stats
    except:
        return None, None


def getEarnings(ticker):
    url = 'https://cloud.iexapis.com/stable/stock/{}/earnings/4/?token={}'.format(ticker, os.environ.get("IEX_TOKEN"))
    earnings = requests.get(url).json()

    return earnings


def checkEarnings(earnings):
    actual = []
    consensus = []
    consistency = []

    for i, report in enumerate(earnings['earnings']):

        actualEps = report['actualEPS'] if 'actualEPS' in report else 0
        surpriseEps = report['EPSSurpriseDollar'] if 'EPSSurpriseDollar' in report else 0

        if (i > 0):
            previous = earnings['earnings'][i - 1]['actualEPS'] if 'actualEPS' in earnings['earnings'][i - 1] else 0
            greater = actualEps > previous if previous != 0 else False
            consistency.append(greater)

        period = report['fiscalPeriod'] if 'fiscalPeriod' in report else 0
        actual.append({period: actualEps})
        consensus.append({period: surpriseEps})

    improvement = False if False in consistency else True

    results = {
        'actual': actual,
        'consensus': consensus,
        'consistency': improvement,
    }

    return results


print('Running...')

Stock = apps.get_model('database', 'Stock')
Earnings = apps.get_model('database', 'Earnings')
Valuation = apps.get_model('database', 'Valuation')
Trend = apps.get_model('database', 'Trend')
Watchlist = apps.get_model('database', 'Watchlist')

results = []
for stock in stocks:
    price, stats = getTrendData(stock.ticker)

    if (price == None or stats == None):
        continue

    week52high = stats['week52high'] if 'week52high' in stats else 0
    if (week52high == 0 or week52high == None):
        continue

    fromHigh = round((price / week52high) * 100, 3)
    ttmEPS = stats['ttmEPS'] if 'ttmEPS' in stats else 0
    if (ttmEPS == 0 or ttmEPS == None):
        continue

    if (stats['day5ChangePercent'] == None or stats['day5ChangePercent'] == 0):
        continue
    day5ChangePercent = stats['day5ChangePercent'] * 100

    # Save to DB
    Stock.objects.filter(ticker=stock.ticker).update(lastPrice=price)
    Valuation.objects.update_or_create(
        stock=stock,
        defaults={'peRatio': stats['peRatio']}
    )
    Trend.objects.update_or_create(
        stock=stock,
        defaults={
            'week52': week52high,
            'day5ChangePercent': stats['day5ChangePercent'],
            'month1ChangePercent': stats['month1ChangePercent'],
            'ytdChangePercent': stats['ytdChangePercent'],
            'day50MovingAvg': stats['day50MovingAvg'],
            'day200MovingAvg': stats['day200MovingAvg'],
            'fromHigh': fromHigh
        }
    )
    Earnings.objects.update_or_create(
        stock=stock,
        defaults={'ttmEPS': ttmEPS}
    )

    if ((fromHigh < 105) and (fromHigh > 95)):
        if (day5ChangePercent > 15):
            earningsData = getEarnings(stock.ticker)
            earningsChecked = checkEarnings(earningsData)

            if (earningsChecked['improvement'] == True):

                Earnings.objects.filter(stock=stock).update(
                    previousEps=earningsChecked['actual'],
                    previousConsensus=earningsChecked['consensus'],
                )

                keyStats = {
                    'week52high': stats['week52high'],
                    'ttmEPS': ttmEPS,
                    'reportedEPS': earningsChecked['actual'],
                    'consensusBeat': earningsChecked['consensus'],
                    'peRatio': stats['peRatio'],
                    'day5ChangePercent': stats['day5ChangePercent'],
                    'month1ChangePercent': stats['month1ChangePercent'],
                    'ytdChangePercent': stats['ytdChangePercent'],
                    'day50MovingAvg': stats['day50MovingAvg'],
                    'day200MovingAvg': stats['day200MovingAvg'],
                    'fromHigh': fromHigh,

                }
                stockData = {
                    'ticker': stock.ticker,
                    'name': stock.name,
                    'lastPrice': price
                }
                stockData.update(keyStats)
                Watchlist.objects.update_or_create(
                    stock=stock,
                    defaults=stockData
                )
                print('{} saved to Watchlist'.format(stock.ticker))
                results.append(stockData)
                printTable(stockData)

if results:
    today = date.today().strftime('%m-%d')
    writeCSV(results, 'trend/trend_chasing_{}.csv'.format(today))


# ---------------------------------------------------------------------------------
# Scrap
# ---------------------------------------------------------------------------------
# 'lastEPS': lastEarnings['actualEPS'] if 'actualEPS' in lastEarnings else 'NA',
# 'consensus': lastEarnings['consensusEPS'] if 'consensusEPS' in lastEarnings else 'NA',
# 'surprise': lastEarnings['EPSSurpriseDollar'] if 'EPSSurpriseDollar' in lastEarnings else 'NA',
# 'yearAgoEPS': lastEarnings['yearAgo'] if 'yearAgo' in lastEarnings else 'NA',
