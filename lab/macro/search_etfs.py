import django
from django.apps import apps
import json
import sys
from ..core.output import printTabs
from .functions import getETFs
from dotenv import load_dotenv
load_dotenv()
django.setup()

def search(query):
    results = []
    etfs = getETFs()
    for etf in etfs:
        if (query in etf.name):
            e = {
                'ticker': etf.ticker,
                'name': etf.name                
            }
            results.append(e)

    printTabs(results)
