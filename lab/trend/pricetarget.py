import django
from django.apps import apps
from dotenv import load_dotenv
import json
import os
import sys
from datetime import date
from .functions import *
from ..core.api import quoteStatsBatchRequest, getPriceTarget
from ..core.output import printFullTable
load_dotenv()
django.setup()

# TODO: Finish price target lookup
def lookup(ticker):
    Stock = apps.get_model('database', 'Stock')
    Trend = apps.get_model('database', 'Trend')
    Watchlist = apps.get_model('database', 'Watchlist')
    
    priceTargets = getPriceTarget(ticker)
    if (priceTargets):
        printFullTable(priceTargets)