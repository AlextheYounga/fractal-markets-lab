import django
from django.apps import apps
from dotenv import load_dotenv
import json
import sys
from datetime import date
from ..fintwit.tweet import send_tweet
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

def formula(data):
    for ticker, prices in data.items():
        past = prices[0]
        # present = 

