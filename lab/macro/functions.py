import django
from ..core.api import getCurrentPrice
from django.apps import apps
import requests
import json
import sys
import os
from dotenv import load_dotenv
load_dotenv()
django.setup()


def getETFs(tickersonly=False):
    Stock = apps.get_model('database', 'Stock')
    stocks = Stock.objects.all()
    etfs = []
    for stock in stocks:
        if ('ETF' in stock.name):
            if (tickersonly):
                etfs.append(stock.ticker)
            else:
                etfs.append(stock)

    return etfs
