import django
from django.apps import apps
import json
import os
import sys
from datetime import date
from .functions import *
from ...database.functions import *
from ...core.functions import *
from ...core.api import quoteStatsBatchRequest
from ...core.output import printTable
from ...core.export import writeCSV
import texttable
django.setup()

unique_stocks = uniqueField('Stock', 'database_stock', 'ticker')
Stock = apps.get_model('database', 'Stock')
Earnings = apps.get_model('database', 'Earnings')
Watchlist = apps.get_model('database', 'Watchlist')

# Main Thread Start
print('Running...')

tickers = []
results = []
for i, stock in enumerate(unique_stocks):
    if ('$' in stock.ticker):  # Removing bad tickers
        continue
    tickers.append(stock.ticker)

chunked_tickers = chunks(tickers, 100)
for i, chunk in enumerate(chunked_tickers):
    batchData = quoteStatsBatchRequest(chunk)  # Check Key Stats Trend Data

    for ticker, batchStats in batchData.items():
        stocks = Stock.objects.filter(ticker=ticker)
        if (type(stocks) == django.db.models.query.QuerySet):
            stock = stocks[0]

        print('Chunk {}: {}'.format(i, ticker))

        if (('quote' not in batchStats) or ('stats' not in batchStats)):
            continue

        if (isinstance(batchStats['quote'], dict) and isinstance(batchStats['stats'], dict)):
            quote = batchStats['quote'] if 'quote' in batchStats else 0
            stats = batchStats['stats'] if 'stats' in batchStats else 0
            if ((isinstance(quote, dict) == False) and (isinstance(stats, dict) == False) and (quote and stats == False)):
                continue
            price = quote['latestPrice'] if ('latestPrice' in quote) else 0
            changeToday = quote['changePercent'] * 100 if ('changePercent' in quote and quote['changePercent']) else 0
            if (isinstance(price, float) and price):
                stocks.update(lastPrice=price)  # Save Stock

            ttmEPS = stats['ttmEPS'] if ('ttmEPS' in stats and stats['ttmEPS']) else 0
            week52high = stats['week52high'] if ('week52high' in stats and stats['week52high']) else 0
            day5ChangePercent = stats['day5ChangePercent'] * 100 if ('day5ChangePercent' in stats and stats['day5ChangePercent']) else 0

            critical = [price, changeToday, week52high, ttmEPS, day5ChangePercent]

            if ((0 in critical)):
                continue

            fromHigh = round((price / week52high) * 100, 3)

            # Save Data to DB
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
                if (changeToday > 8):
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
                            watchlists = Watchlist.objects.filter(stock=stock)
                            if (watchlists.count() == 0):
                                stockData['stock'] = stock
                                Watchlist.objects.create(**stockData)
                            else:
                                watchlists.update(**stockData)

                            print('{} saved to Watchlist'.format(ticker))
                            results.append(stockData)
                            printTable(stockData)

if results:
    today = date.today().strftime('%m-%d')
    writeCSV(results, 'trend/trend_chasing_{}.csv'.format(today))
