from dotenv import load_dotenv
import json
import os
import sys
from datetime import date
from .functions import *
from ..core.api import quoteStatsBatchRequest, getPriceTarget
from ..core.output import printFullTable
load_dotenv()


# TODO: Finish price target lookup
# def lookup(ticker):
#     Stock = apps.get_model('database', 'Stock')
#     Watchlist = apps.get_model('database', 'Watchlist')
    
#     priceTargets = getPriceTarget(ticker)
#     if (priceTargets):
#         printFullTable(priceTargets)