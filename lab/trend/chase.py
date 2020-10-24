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
from ..shared.output import printTable
from ..shared.export import writeCSV
import texttable
django.setup()

stocks = uniqueField('Stock', 'database_stock', 'ticker')

# Main Thread Start
print('Running...')

Stock = apps.get_model('database', 'Stock')
Earnings = apps.get_model('database', 'Earnings')
Watchlist = apps.get_model('database', 'Watchlist')

results = []
for i, stock in enumerate(stocks):
    if (i != 23):
        continue
    print('{}: {}'.format(i, stock.ticker))
    price, stats = getTrendData(stock.ticker)  # Check Key Stats Trend Data
    if ((type(price) != float) or (stats and type(stats) != dict)):
        continue
    ttmEPS = stats['ttmEPS'] if 'ttmEPS' in stats else 0
    week52high = stats['week52high'] if 'week52high' in stats else 0
    day5ChangePercent = stats['day5ChangePercent'] * 100 if 'day5ChangePercent' in stats else 0
    critical = [week52high, ttmEPS, day5ChangePercent]
    print(critical)
    sys.exit()
    for data in critical:
        if (data == 0 or isinstance(data, (float, int)) == False):
            continue

    fromHigh = round((price / week52high) * 100, 3)

    # Save Data to DB
    Stock.objects.filter(ticker=stock.ticker).update(lastPrice=price)  # Save Stock

    data_for_db = {
        'Valuation':  {
            'stock': stock,
            'peRatio': stats['peRatio'],
        },
        'Trend': {
            'stock': stock,
            'week52': week52high,
            'day5ChangePercent': stats['day5ChangePercent'],
            'month1ChangePercent': stats['month1ChangePercent'],
            'ytdChangePercent': stats['ytdChangePercent'],
            'day50MovingAvg': stats['day50MovingAvg'],
            'day200MovingAvg': stats['day200MovingAvg'],
            'fromHigh': fromHigh
        },
        'Earnings': {
            'stock': stock,
            'ttmEPS': ttmEPS
        },
    }

    saveDynamic(data_for_db, stock)

    if ((fromHigh < 105) and (fromHigh > 95)):
        if (day5ChangePercent > 10):
            earningsData = getEarnings(stock.ticker)
            if (earningsData and isinstance(earningsData, dict)):
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
