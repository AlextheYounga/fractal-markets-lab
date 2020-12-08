import django
from django.apps import apps
import pandas as pd
import json
from ..core.output import writeCSV
import sys

JSON = "lab/correlations/output/json/correlations.json"


def json_to_csv():
    output = {}
    with open(JSON) as jsonfile:
        correlations = json.loads(jsonfile.read())

        for cl, data in correlations.items():
            tickers = cl.split('/')
            t1 = tickers.pop(0)
            t2 = tickers[0]
            if (t1 not in output):
                output[t1] = []

            d = {
                'ticker': t1,
                'comparand': t2,
                'rvalue': data[0],
                'datapoints': data[1]
            }
            output[t1].append(d)

    for ticker, data in output.items():        
        writeCSV(data, 'lab/correlations/output/csv/{}.csv'.format(ticker))
        print('Generated csv for {}'.format(ticker))
