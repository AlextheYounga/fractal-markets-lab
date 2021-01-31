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
Correlation = apps.get_model('database', 'Correlation')
HistoricalPrices = apps.get_model('database', 'HistoricalPrices')
correlations = Correlation.objects.all()
stocks = Stock.objects.all()

def calculate_datapoints(corr):
    h1 = HistoricalPrices.objects.get(stock=corr.stock)
    s2 = Stock.objects.get(ticker=corr.comparand)
    h2 = HistoricalPrices.objects.get(stock=s2)

    counts = [len(h1.prices), len(h2.prices)]
    dp = min(counts)

    return dp


for corr in correlations:    
    t1 = corr.stock.ticker
    t2 = corr.comparand
    rv = corr.rvalue
    if (corr.datapoints):
        dp = corr.datapoints
    else:
        dp = calculate_datapoints(corr)
        
    print(t1+'-'+t2)

    r.set('correlation-'+t1+'-'+t2+'-rvalue', (corr.rvalue if corr.rvalue else ""))
    r.set('correlation-'+t1+'-'+t2+'-datapoints', dp)
    
