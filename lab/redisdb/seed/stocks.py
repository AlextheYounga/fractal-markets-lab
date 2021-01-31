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
stocks = Stock.objects.all()

for stock in stocks:    
    ticker = stock.ticker
    print(ticker)

    # Stocks    
    r.set('stock-'+ticker+'-name', (stock.name if stock.name else ""))
    