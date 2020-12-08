import django
from django.apps import apps
from ..core.functions import extract_data, chunks
from ..core.output import printFullTable, writeCSV
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import json
import sys
import os
from dotenv import load_dotenv
load_dotenv()
django.setup()

Stock = apps.get_model('database', 'Stock')
HistoricalPrices = apps.get_model('database', 'HistoricalPrices')
Correlations = apps.get_model('database', 'Correlation')
JSON = "lab/correlations/output/json/correlations.json"


def is_short(n):
    blacklist = ['Short', 'Inverse', 'Bear', 'Decline', 'Tail']
    for b in blacklist:
        if (b in n):
            return True
    return False


def print_correlation(corrs):
    table_data = [['Company', 'Comparand', 'Rvalue', 'Points']]
    csvdata = []
    for etf in corrs[:100]:
        comparand = Stock.objects.get(ticker=etf.comparand)
        if (is_short(etf.stock.name)):
            continue
        if (is_short(comparand.name)):
            continue
        c1 = "{}({})".format(etf.stock.name, etf.stock.ticker)
        c2 = "{}({})".format(comparand.name, comparand.ticker)
        rv = "{}".format(etf.rvalue)
        dp = count_data_points(etf.stock.ticker, comparand.ticker)

        table_data.append([c1, c2, rv, dp])
        csvd = {'Company': c1, 'Comparand': c2, 'Rvalue': rv, 'Points': dp}
        csvdata.append(csvd)

    printFullTable(table_data, widths=7)
    writeCSV(csvdata, "lab/correlations/output/lookup/results.csv", append=True)
    return 'Done'


def inverse_correlations(n, src='database'):
    if (src == 'database'):
        correlations = Correlations.objects.filter(rvalue__lte=n)
        print_correlation(correlations)

    # TODO Get it set up to run on just json, db is too slow
    if (src == 'json'):
        results = []
        with open(JSON) as jsonfile:
            correlations = json.loads(jsonfile.read())
            for ticker, data in correlations.items():
                stock = Stock.objects.get(ticker=ticker)
                for item in data:
                    print(item)
                    sys.exit()


def positive_correlations(n, src='database'):
    if (src == 'database'):
        correlations = Correlations.objects.filter(rvalue__gte=n)
        print_correlation(correlations)


def print_lookup(corrs):
    table_data = [['Ticker', 'Comparand', 'Rvalue', 'Points']]
    csvdata = []
    for etf in corrs:
        if (etf.rvalue):
            # if ((etf.rvalue >= 0.98 and etf.rvalue < 1) or (etf.rvalue <= -0.98 and etf.rvalue > -1)):
            if (etf.rvalue <= -0.93 and etf.rvalue > -1):
                comparand = Stock.objects.get(ticker=etf.comparand)

                if ((not is_short(etf.stock.name)) and (not is_short(comparand.name))):
                    dp = min(
                        HistoricalPrices.objects.get(stock=etf.stock).datapoints,
                        HistoricalPrices.objects.get(stock=comparand).datapoints
                    )
                    if (dp > 759):
                        print(etf.stock.ticker, comparand.ticker)
                        c1 = "{}({})".format(etf.stock.name, etf.stock.ticker)
                        c2 = "{}({})".format(comparand.name, comparand.ticker)
                        rv = "{}".format(etf.rvalue)

                        table_data.append([c1, c2, rv, dp])
                        csvd = {'Company': c1, 'Comparand': c2, 'Rvalue': rv, 'Points': dp}
                        csvdata.append(csvd)

    # printFullTable(table_data, widths=7)
    if (csvdata):
        writeCSV(csvdata, "lab/correlations/output/lookup/results.csv")
        return 'Done'


def get_ticker_correlations(ticker):
    stock = Stock.objects.get(ticker=ticker)
    correlations = Correlations.objects.filter(stock=stock)
    print_lookup(correlations)


def get_significant_correlations():
    correlations = Correlations.objects.all()
    print_lookup(correlations)
