import django
from django.apps import apps
from dotenv import load_dotenv
import json
import os
import sys
from datetime import date
from .functions import *
from ..core.functions import chunks
from ..core.api import quoteStatsBatchRequest, getStockInfo
from ..core.output import printTable
from ..core.export import writeCSV
import texttable
load_dotenv()
django.setup()


Stock = apps.get_model('database', 'Stock')
MacroTrends = apps.get_model('database', 'MacroTrend')
Watchlist = apps.get_model('database', 'Watchlist')

results = []
etfs = getETFs(True)
chunked_etfs = chunks(etfs, 100)
for i, chunk in enumerate(chunked_etfs):
    batch = quoteStatsBatchRequest(chunk)
    for ticker, stockinfo in batch.items():
        print('Chunk {}: {}'.format(i, ticker))

        if (stockinfo.get('quote', False) and stockinfo.get('stats', False)):
            quote = stockinfo.get('quote')
            stats = stockinfo.get('stats')
            price = quote.get('latestPrice', 0)

            if ((price) and (isinstance(price, float)) and (price > 10)):
                etf, created = Stock.objects.update_or_create(
                    ticker=ticker,
                    defaults={'lastPrice': price},
                )
            else:
                continue

            day5ChangePercent = stats['day5ChangePercent'] * 100 if ('day5ChangePercent' in stats and stats['day5ChangePercent']) else None
            changeToday = quote['changePercent'] * 100 if ('changePercent' in quote and quote['changePercent']) else 0
            previousVolume = quote['previousVolume'] if ('previousVolume' in quote and quote['previousVolume']) else 0
            month1ChangePercent = stats['month1ChangePercent'] * 100 if ('month1ChangePercent' in stats and stats['month1ChangePercent']) else None
            # Critical
            volume = quote['volume'] if ('volume' in quote and quote['volume']) else 0
            avg30Volume = stats['avg30Volume'] if ('avg30Volume' in stats and stats['avg30Volume']) else None
            week52high = stats['week52high'] if ('week52high' in stats and stats['week52high']) else 0
            month3ChangePercent = stats['month3ChangePercent'] * 100 if ('month3ChangePercent' in stats and stats['month3ChangePercent']) else None
            day50MovingAvg = stats['day50MovingAvg'] if ('day50MovingAvg' in stats and stats['day50MovingAvg']) else None

            critical = [volume, avg30Volume, week52high, day50MovingAvg]

            if ((0 in critical)):
                continue

            fromHigh = round((price / week52high) * 100, 3)

            if ((fromHigh < 100) and (fromHigh > 70)):
                if (price > day50MovingAvg):
                    if ((volume / avg30Volume) > 3):

                        keyStats = {
                            'week52': stats['week52high'],
                            'day5ChangePercent': stats['day5ChangePercent'],
                            'month3ChangePercent': stats['month3ChangePercent'],
                            'ytdChangePercent': stats['ytdChangePercent'],                            
                            'avg30Volume': "{}K".format(avg30Volume / 1000),
                            'month1ChangePercent': month1ChangePercent,
                            'month3ChangePercent': month3ChangePercent,
                            'day50MovingAvg': day50MovingAvg,
                            'day200MovingAvg': stats['day200MovingAvg'],
                            'fromHigh': fromHigh,
                        }

                        stockData = {
                            'ticker': ticker,
                            'name': etf.name,
                            'lastPrice': price
                        }
                        stockData.update(keyStats)

                        # Save to Macro
                        MacroTrends.objects.update_or_create(
                            etf=etf,
                            defaults=stockData
                        )
                        stockData['volume'] = "{}K".format(volume / 1000)
                        results.append(stockData)
                        printTable(stockData)

if results:
    today = date.today().strftime('%m-%d')
    writeCSV(results, 'macro/etfs_{}.csv'.format(today))
