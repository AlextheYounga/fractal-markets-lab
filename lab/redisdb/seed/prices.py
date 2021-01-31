import django
from django.apps import apps
import json
import redis
import sys
import os
from dotenv import load_dotenv
load_dotenv()
django.setup()

r = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)

Stock = apps.get_model('database', 'Stock')
HistoricalPrices = apps.get_model('database', 'HistoricalPrices')

stocks = Stock.objects.all()

for stock in stocks:    
    ticker = stock.ticker
    print(ticker)

    if (HistoricalPrices.objects.filter(stock=stock).count() != 0):
        hp = HistoricalPrices.objects.get(stock=stock)
        r.set('stock-'+ticker+'-prices', (json.dumps(hp.prices) if hp.prices else ""))
        r.set('stock-'+ticker+'-prices-datapoints', (hp.datapoints if hp.datapoints else ""))
    
