import django
from django.apps import apps
import json
import sys
import os
django.setup()

HistoricalPrices = apps.get_model('database', 'HistoricalPrices')
histprices = HistoricalPrices.objects.all()

for hp in histprices:
    print("Seeding", hp.stock.ticker)
    hp.datapoints = len(hp.prices)
    hp.save()