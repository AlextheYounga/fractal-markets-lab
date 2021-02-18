import django
from django.apps import apps
import json
import sys
import os
django.setup()


def is_short(n):
    blacklist = ['Short', 'Inverse', 'Bear', 'Decline', 'Tail']
    for b in blacklist:
        if (b in n):
            return True
    return False


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
