import django
from django.apps import apps
import json
import sys
import os
from dotenv import load_dotenv
load_dotenv()
django.setup()

HistoricalPrices = apps.get_model('database', 'HistoricalPrices')
Correlation = apps.get_model('database', 'Correlation')
Stock = apps.get_model('database', 'Stock')
correlations = Correlation.objects.all()
histprices = HistoricalPrices.objects.all()

# for hp in histprices:
#     if (hp.datapoints == None):
#         print("Seeding", hp.stock.ticker)
#         hp.datapoints = len(hp.prices)
#         hp.save()

for corr in correlations:
    if (corr.datapoints == None):
        print("Seeding {} - {}".format(corr.stock.ticker, corr.comparand))
        h1 = HistoricalPrices.objects.get(stock=corr.stock)
        s2 = Stock.objects.get(ticker=corr.comparand)
        h2 = HistoricalPrices.objects.get(stock=s2)

        counts = [len(h1.prices), len(h2.prices)]
        corr.datapoints = min(counts)
        corr.save()