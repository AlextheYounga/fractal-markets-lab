import django
from django.apps import apps
from dotenv import load_dotenv
import json
import sys
from datetime import date
from ..fintwit.tweet import send_tweet
from .methodology import SECTORS
from ..core.functions import chunks, extract_data
from ..core.api import batchHistoricalData, getStockInfo
from ..core.output import printFullTable, writeCSV
load_dotenv()
django.setup()



def fetch_prices(timeframe='1y'):
    prices = {}
    batch = batchHistoricalData(SECTORS, timeframe, priceOnly=True, sandbox=True)
    for ticker, etf in batch.items():
        prices[ticker] = extract_data(etf['chart'], 'close')

    return prices
        

