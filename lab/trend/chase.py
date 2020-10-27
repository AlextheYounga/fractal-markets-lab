import django
from django.apps import apps
import json
import os
import sys
from datetime import date
from .functions import *
from ..core.functions import chunks
from ..core.api import quoteStatsBatchRequest
from ..core.output import printTable
from ..core.export import writeCSV
import texttable
django.setup()

Stock = apps.get_model('database', 'Stock')
Earnings = apps.get_model('database', 'Earnings')
Watchlist = apps.get_model('database', 'Watchlist')

# Main Thread Start
print('Running...')

results = []
tickers = Stock.objects.all().values_list('ticker', flat=True)

chunked_tickers = chunks(tickers, 100)
for i, chunk in enumerate(chunked_tickers):
    batch = quoteStatsBatchRequest(chunk)

    for ticker, stockinfo in batch.items():
        print('Chunk {}: {}'.format(i, ticker))

        if (stockinfo.get('quote', False) and stockinfo.get('stats', False)):
            quote = stockinfo.get('quote')
            stats = stockinfo.get('stats')

            price = quote.get('latestPrice', 0)

            if (price and isinstance(price, float)):
                stock, created = Stock.objects.update_or_create(
                    ticker=ticker,
                    defaults={'lastPrice': price},
                )
            else:
                continue

            ttmEPS = stats.get('ttmEPS', 0)
            week52high = stats.get('week52high', 0)
            changeToday = quote.get('changePercent', 0) * 100 if (quote.get('changePercent')) else 0
            day5ChangePercent = stats.get('day5ChangePercent', 0) * 100 if (stats.get('day5ChangePercent')) else 0

            critical = [changeToday, week52high, ttmEPS, day5ChangePercent]

            if ((0 in critical)):
                continue

            fromHigh = round((price / week52high) * 100, 3)

            # Save Data to DB
            data_for_db = {
                'Valuation':  {
                    'peRatio': stats['peRatio'],
                },
                'Trend': {
                    'week52': week52high,
                    'day5ChangePercent': stats['day5ChangePercent'],
                    'month1ChangePercent': stats.get('month1ChangePercent', None),
                    'ytdChangePercent': stats.get('ytdChangePercent', None),
                    'day50MovingAvg': stats.get('day50MovingAvg', None),
                    'day200MovingAvg': stats.get('day200MovingAvg', None),
                    'fromHigh': fromHigh
                },
                'Earnings': {
                    'ttmEPS': ttmEPS
                },
            }
            
            dynamicUpdateCreate(data_for_db, stock)

            if ((fromHigh < 105) and (fromHigh > 95)):
                if (changeToday > 10):
                    earningsData = getEarnings(ticker)
                    if (earningsData and isinstance(earningsData, dict)):
                        print('{} ---- Checking Earnings ----'.format(ticker))
                        earningsChecked = checkEarnings(earningsData)

                        # Save Earnings to DB
                        Earnings.objects.filter(stock=stock).update(
                            reportedEPS=earningsChecked['actual'],
                            reportedConsensus=earningsChecked['consensus'],
                        )

                        if (earningsChecked['improvement'] == True):
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
                                'ticker': ticker,
                                'name': stock.name,
                                'lastPrice': price
                            }
                            stockData.update(keyStats)

                            # Save to Watchlist
                            Watchlist.objects.update_or_create(
                                stock=stock,
                                defaults=stockData
                            )

                            print('{} saved to Watchlist'.format(ticker))
                            results.append(stockData)
                            printTable(stockData)

if results:
    today = date.today().strftime('%m-%d')
    writeCSV(results, 'trend/trend_chasing_{}.csv'.format(today))
