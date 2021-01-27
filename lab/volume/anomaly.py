import django
from django.apps import apps
from dotenv import load_dotenv
import json
import sys
from datetime import date
from ..database.functions import dynamicUpdateCreate
from ..core.functions import chunks, dataSanityCheck
from ..core.api import batchHistoricalData
from ..core.output import printFullTable, writeCSV
from ..fintwit.tweet import send_tweet
load_dotenv()
django.setup()

Stock = apps.get_model('database', 'Stock')
Trend = apps.get_model('database', 'Trend')
Watchlist = apps.get_model('database', 'Watchlist')

print('Running...')

results = []
tickers = Stock.objects.all().values_list('ticker', flat=True)

chunked_tickers = chunks(tickers, 100)
for i, chunk in enumerate(chunked_tickers):
    batch = batchHistoricalData(chunk, '5d', priceOnly=True)

    for ticker, info in batch.items():
        print('Chunk {}: {}'.format(i, ticker))
        if (info.get('chart', False)):
            chart = info['chart']
            price = chart[-1].get('close', 0)
            priceFirst = chart[0].get('close', 0)
            volumeFirst = round(dataSanityCheck(chart[0], 'volume'), 2)
            volumeToday = round(dataSanityCheck(chart[-1], 'volume'), 2)
            changeToday = round(dataSanityCheck(chart[-1], 'changePercent'), 2)
            changePercent5d = round((priceFirst - price) / priceFirst)

            if ((price) and (isinstance(price, float) and (price > 0.5))):
                stock, created = Stock.objects.update_or_create(
                    ticker=ticker,
                    defaults={'lastPrice': price},
                )
            else:
                continue
            
            if (0 in [volumeFirst, volumeToday, changeToday]):
                continue

            for vol in [volumeFirst, volumeToday]:
                if ((vol / 1000) < 1):
                    continue
        
            if ((volumeToday / volumeFirst) > 10):
                stockData = {
                    'ticker': ticker,
                    'lastPrice': price,
                    'volumeToday': "{}K".format(round(volumeToday / 1000, 4)),
                    'volume5dAgo': "{}K".format(round(volumeFirst / 1000, 4)),
                    'volumeIncrease': round(volumeToday / volumeFirst),
                    'changeToday': "{}%".format(round(changeToday * 100, 2)),
                    '5dPercentChange': "{}%".format(round(((price - priceFirst) / priceFirst) * 100, 2))
                }
                results.append(stockData)

            
if results:
    printFullTable(results, struct='dictlist')

    today = date.today().strftime('%m-%d')
    writeCSV(results, 'lab/volume/output/anomalies/anomalies{}.csv'.format(today))

    
        
