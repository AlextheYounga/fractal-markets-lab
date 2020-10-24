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
    try:
        url = 'https://cloud.iexapis.com/stable/stock/{}/earnings/4/?token={}'.format(ticker, os.environ.get("IEX_TOKEN"))
        earnings = requests.get(url).json()
    except:
        return None

    return earnings


def checkEarnings(earnings):
    actual = []
    consensus = []
    consistency = []

    for i, report in enumerate(earnings['earnings']):

        actualEps = report['actualEPS'] if 'actualEPS' in report else 0
        surpriseEps = report['EPSSurpriseDollar'] if 'EPSSurpriseDollar' in report else 0

        if (i > 0):
            previous = earnings['earnings'][i - 1]['actualEPS'] if ('actualEPS' in earnings['earnings'][i - 1]) else 0
            greater = actualEps > previous if (previous != 0) else False
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
    print(stock.ticker)
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

    # Save Stock to DB
    Stock.objects.filter(ticker=stock.ticker).update(lastPrice=price)
    # Save Valuations to DB
    valuations = Valuation.objects.filter(stock=stock)
    if (valuations.count() == 0):
        Valuation(stock=stock, peRatio=stats['peRatio']).save()
    else:
        valuations.update(peRatio=stats['peRatio'])
    # Save Trends to DB
    trends = Trend.objects.filter(stock=stock)
    trend_data = {
        'stock': stock,
        'week52': week52high,
        'day5ChangePercent': stats['day5ChangePercent'],
        'month1ChangePercent': stats['month1ChangePercent'],
        'ytdChangePercent': stats['ytdChangePercent'],
        'day50MovingAvg': stats['day50MovingAvg'],
        'day200MovingAvg': stats['day200MovingAvg'],
        'fromHigh': fromHigh
    }
    if (trends.count() == 0):
        Trend.objects.create(**trend_data)
    else:
        del trend_data['stock']
        trends.update(**trend_data)
    # Save Earnings to DB
    earnings_records = Earnings.objects.filter(stock=stock)
    if (earnings_records.count() == 0):
        Earnings(
            stock=stock,
            ttmEPS=ttmEPS
        ).save()
    else:
        Earnings.objects.update(ttmEPS=ttmEPS)

    if ((fromHigh < 105) and (fromHigh > 95)):
        if (day5ChangePercent > 15):
            earningsData = getEarnings(stock.ticker)
            if (earningsData != None):
                earningsChecked = checkEarnings(earningsData)

                if (earningsChecked['consistency'] == True):
                    Earnings.objects.filter(stock=stock).update(
                        reportedEPS=earningsChecked['actual'],
                        reportedConsensus=earningsChecked['consensus'],
                    )

                    keyStats = {
                        'week52': stats['week52high'],
                        'ttmEPS': ttmEPS,
                        'reportedEPS': earningsChecked['actual'],
                        'reportedConsensus': earningsChecked['consensus'],
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
                    watchlists = Watchlist.objects.filter(stock=stock)
                    if (watchlists.count() == 0):
                        stockData['stock'] = stock
                        Watchlist.objects.create(**stockData)
                    else:
                        watchlists.update(**stockData)
                    print('{} saved to Watchlist'.format(stock.ticker))
                    results.append(stockData)
                    printTable(stockData)
                    sys.exit()

if results:
    today = date.today().strftime('%m-%d')
    writeCSV(results, 'trend/trend_chasing_{}.csv'.format(today))

