import django
from django.apps import apps
from ..core.functions import extract_data, chunks
from datetime import datetime
import json
import sys
import os
from .functions import is_short
from ..core.output import printFullTable
from dotenv import load_dotenv

load_dotenv()
django.setup()

Stock = apps.get_model('database', 'Stock')
Correlation = apps.get_model('database', 'Correlation')


def print_correlation(corrs):
    for i in corrs[:100]:
        comparand = Stock.objects.get(ticker=i.comparand)
        if (is_short(i.stock.name)):
            continue
        if (is_short(comparand.name)):
            continue
        print("{}({}) - {}({}): {}".format(
            i.stock.name,
            i.stock.ticker,
            comparand.name,
            comparand.ticker,
            i.rvalue))


def print_lookup(corr):
    table_data = [['Ticker', 'Comparand', 'Rvalue', 'Points']]
    c1 = corr.stock.ticker
    c2 = corr.comparand
    rv = corr.rvalue
    dp = corr.datapoints

    table_data.append([c1, c2, rv, dp])
    printFullTable(table_data, widths=7)


def lookup(t1, t2):
    stock = Stock.objects.get(ticker=t1)
    correlation = Correlation.objects.get(stock=stock, comparand=t2)
    if (correlation):
        print(correlation)
        return print_lookup(correlation)

    print('No correlation record found')
        


def positive_correlations(n, src='database'):
    if (src == 'database'):
        correlations = Correlation.objects.filter(rvalue__gte=n)
        print_correlation(correlations)
