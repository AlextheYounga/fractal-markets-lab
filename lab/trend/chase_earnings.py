import django
from django.apps import apps
from dotenv import load_dotenv
import json
import time
import sys
from datetime import date
from .functions import *
from ..redisdb.controller import rdb_save_stock
from ..core.functions import chunks, dataSanityCheck
from ..core.api.historical import getHistoricalEarnings
from ..core.api.batch import quoteStatsBatchRequest
from ..core.api.stats import getPriceTarget
from ..core.output import printFullTable, writeCSV
from ..fintwit.tweet import send_tweet
load_dotenv()
django.setup()

Stock = apps.get_model('database', 'Stock')
Watchlist = apps.get_model('database', 'Watchlist')

# Main Thread Start
print('Running...')

results = []
tickers = Stock.objects.all().values_list('ticker', flat=True)

chunked_tickers = chunks(tickers, 100)
for i, chunk in enumerate(chunked_tickers):
    time.sleep(1)
    batch = quoteStatsBatchRequest(chunk)

    for ticker, stockinfo in batch.items():
        print('Chunk {}: {}'.format(i, ticker))

        if (stockinfo.get('quote', False) and stockinfo.get('stats', False)):
            quote = stockinfo.get('quote')
            stats = stockinfo.get('stats')

            price = quote.get('latestPrice', 0)

            if (price and isinstance(price, float)):
                month1ChangePercent = round(dataSanityCheck(stats, 'month1ChangePercent') * 100, 2)
                ytdChangePercent = round(dataSanityCheck(stats, 'ytdChangePercent') * 100, 2)

                # Critical
                ttmEPS = dataSanityCheck(stats, 'ttmEPS')
                week52high = dataSanityCheck(stats, 'week52high')
                changeToday = round(dataSanityCheck(quote, 'changePercent') * 100, 2)
                day5ChangePercent = round(dataSanityCheck(stats, 'day5ChangePercent') * 100, 2)
                critical = [changeToday, week52high, ttmEPS, day5ChangePercent]

                if ((0 in critical)):
                    continue

                fromHigh = round((price / week52high) * 100, 3)

                # Save Data to DB
                rdb_data = {                    
                    'peRatio': stats.get('peRatio', None),
                    'week52': week52high,
                    'day5ChangePercent': day5ChangePercent if day5ChangePercent else None,
                    'month1ChangePercent': month1ChangePercent if month1ChangePercent else None,
                    'ytdChangePercent': ytdChangePercent if ytdChangePercent else None,
                    'day50MovingAvg': stats.get('day50MovingAvg', None),
                    'day200MovingAvg': stats.get('day200MovingAvg', None),
                    'fromHigh': fromHigh,
                    'ttmEPS': ttmEPS,
                }

                rdb_save_stock(ticker, rdb_data)

                if ((fromHigh < 105) and (fromHigh > 95)):
                    if (changeToday > 10):
                        earningsData = getHistoricalEarnings(ticker)
                        if (earningsData and isinstance(earningsData, dict)):
                            print('{} ---- Checking Earnings ----'.format(ticker))
                            earningsChecked = checkEarnings(earningsData)
                            if (isinstance(earningsChecked, dict) and earningsChecked['actual'] and earningsChecked['consensus']):
                                # Save Earnings to DB
                                if (earningsChecked['improvement'] == True):

                                    keyStats = {}
                                    for model, data in rdb_data.items():
                                        keyStats.update(data)
                                    keyStats.update({
                                        'reportedEPS': earningsChecked['actual'],
                                        'reportedConsensus': earningsChecked['consensus'],
                                    })
                                    stockData = {
                                        'ticker': ticker,
                                        'name': quote['companyName'],
                                        'lastPrice': price
                                    }
                                    stockData.update(keyStats)

                                    # Save to Watchlist
                                    Watchlist.objects.update_or_create(
                                        ticker=ticker,
                                        defaults=stockData
                                    )

                                    print('{} saved to Watchlist'.format(ticker))
                                    results.append(stockData)

if results:
    today = date.today().strftime('%m-%d')
    writeCSV(results, 'lab/trend/output/earnings/trend_chasing_{}.csv'.format(today))

    printFullTable(results, struct='dictlist')

    # Tweet
    tweet = ""
    for i, data in enumerate(results):
        ticker = '${}'.format(data['ticker'])
        ttmEPS = data['ttmEPS']
        day5ChangePercent = data['day5ChangePercent']
        tweet_data = "{} ttmEPS: {}, 5dayChange: {} \n".format(ticker, ttmEPS, day5ChangePercent)
        tweet = tweet + tweet_data

    send_tweet(tweet, True)
