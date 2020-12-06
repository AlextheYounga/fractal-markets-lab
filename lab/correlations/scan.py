import django
from django.apps import apps
from ..core.functions import extract_data, chunks
from ..core.output import writeCSV
from .functions import count_data_points
from datetime import datetime, timedelta
from multiprocessing import Pool, cpu_count
import pandas as pd
import numpy as np
import json
import sys
import os
from dotenv import load_dotenv
from ..twitter.tweet import send_tweet
load_dotenv()
django.setup()
FILES = "lab/correlations/output/files"
JSON = "lab/correlations/output/json/correlations.json"
CSV = "lab/correlations/output/csv"

HistoricalPrices = apps.get_model('database', 'HistoricalPrices')
priceobjs = HistoricalPrices.objects.all()
badset = ['GCOW', 'FAAR']
json_output = {}


def scan_output_folder(output):
    if (output):
        if (output == 'files'):
            files = os.listdir(FILES)
        if (output == 'csv'):
            files = os.listdir(CSV)
        return [f.split('.').pop(0) for f in files]


def redundant_correlation(t1, t2, output):
    if (output == 'json'):
        if (t2 in json_output and json_output[t2]):
            for data in json_output[t2]:
                if (data['comparand'] == t1):
                    return True
        return False
    if (output == 'files'):
        if (t1 in scan_output_folder()):
            with open(os.path.join(FILES, "{}.txt".format(t1))) as txtfile:
                correlations = json.loads(txtfile.read())
                for corrs in correlations:
                    if (corrs['comparand'] == t2):
                        return True
        return False


def correct_lengths(h1, h2):
    objs = [h1.prices, h2.prices]
    smallest = [k for k, v in enumerate(objs) if len(v) == min([len(h1.prices), len(h2.prices)])][0]
    smol = objs.pop(smallest)
    big = objs[0]

    trimmedY = big[-len(smol):]

    x = extract_data(smol, 'close')
    y = extract_data(trimmedY, 'close')
    return x, y


def run_correlation(h1, output='files'):
    json_output[h1.stock.ticker] = []
    correlations = []

    for h2 in priceobjs:
        if h1 == h2:
            continue
        if (h2.stock.ticker in badset):
            continue
        if (redundant_correlation(h1.stock.ticker, h2.stock.ticker, output)):
            continue

        if ((len(h1.prices) == len(h2.prices)) == False):
            x, y = correct_lengths(h1, h2)
        else:
            x = extract_data(h1.prices, 'close')
            y = extract_data(h2.prices, 'close')

        try:
            r = np.corrcoef(x, y)
        except:
            print("Failed to correlate {} and {}. Skipping.".format(h1.stock.ticker, h2.stock.ticker))
            continue
        rv = r[0, 1]
        dpoints = count_data_points(h1.stock.ticker, h2.stock.ticker)
        result = {'comparand': h2.stock.ticker, 'rvalue': rv, 'datapoints': dpoints}
        if (output != 'json'):
            correlations.append(result)
        else:
            json_output[h1.stock.ticker].append(result)

    if (output == 'files'):
        with open(os.path.join(FILES, '{}.txt'.format(h1.stock.ticker)), 'w') as txtfile:
            json.dump(correlations, txtfile)
    if (output == 'csv'):
        writeCSV(correlations, 'lab/correlations/output/csv/{}.csv'.format(h1.stock.ticker))


def scan_for_correlations(output='files'):
    print('Running...')
    for h in priceobjs:
        if (output != 'json'):
            if (h.stock.ticker in scan_output_folder(output)):
                continue
        if (h.stock.ticker in badset):
            continue
        print("Mass Correlating: {}".format(h.stock.ticker))
        run_correlation(h, output)

    if (output == 'json'):
        with open(JSON, 'w') as json_file:
            json.dump(json_output, json_file)
