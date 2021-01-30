import django
from django.apps import apps
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import statistics
import json
import sys
from datetime import date
from ..database.hp.update_prices import update_prices, batch_refresh_prices
from ..core.functions import chunks
from ..core.api import quoteStatsBatchRequest, getStockInfo
from ..core.output import printFullTable, writeCSV
load_dotenv()
django.setup()


def sectors():
    return [
        'XLY',
        'XLP',
        'XLE',
        'XLF',
        'XLV',
        'XLI',
        'XLB',
        'XLRE',
        'XLK',
        'XLC',
        'XLU',
        'XME',
        'VNQ',
        'GDX',
        'AMLP',
        'ITB',
        'OIH',
        'KRE',
        'XRT',
        'MOO',
        'FDN',
        'IBB',
        'SMH',
        'XOP',
        'PBW',
        'KIE',
        'PHO',
        'IGV'
    ]


def trim_data(data):
    trimmed = {}
    COUNT = len(sectors())
    for date, prices in data.items():
        if (len(prices) != COUNT):
            continue
        trimmed[date] = prices

    return trimmed


def collect_data(update=False):
    HistoricalPrices = apps.get_model('database', 'HistoricalPrices')
    Stock = apps.get_model('database', 'Stock')

    data = {}    

    for ticker in sectors():
        print(ticker)

        stock = Stock.objects.get(ticker=ticker)

        if (update):
            update_prices(stock)
        
        hp = HistoricalPrices.objects.get(stock=stock)

        for row in hp.prices:
            if (row['date'] not in data):
                data[row['date']] = []

            data[row['date']].append(row['close'])

    data = trim_data(data)

    return data


def formula():
    index = {}
    data = collect_data()
    for day, prices in data.items():
        avg = statistics.mean(prices)
        index[day] = avg
    
    
    return index
