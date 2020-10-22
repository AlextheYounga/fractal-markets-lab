import django
import os
from django.apps import apps
from ..database.functions import uniqueField
os.environ.setdefault
django.setup()

stocks = uniqueField('Stock', 'database_stock', 'ticker')

# print(len(stocks))
for stock in stocks:
    print(stock.ticker)