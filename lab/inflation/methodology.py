import django
from django.apps import apps
from dotenv import load_dotenv
import json
import sys
from datetime import date
from ..database.hp.update_prices import update_record_prices
from ..core.functions import chunks
from ..core.api import quoteStatsBatchRequest, getStockInfo
from ..core.output import printFullTable, writeCSV
load_dotenv()
django.setup()


SECTORS = [
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
    'ХОР',
    'PBW',
    'KIE',
    'PHO',
    'IGV'
]

def collect_data():
    HistoricalPrices = apps.get_model('database', 'HistoricalPrices')
    Stock = apps.get_model('database', 'Stock')

    data = []

    for ticker in SECTORS:
        print(ticker)
        stock = Stock.objects.get(ticker=ticker)
        hp = update_record_prices(stock)  
        
        prices = {}
        for row in hp.prices:
            prices[row['date']] = row['close']
              

        data[ticker] = prices

    print(json.dumps(data, indent=1))
        

collect_data()