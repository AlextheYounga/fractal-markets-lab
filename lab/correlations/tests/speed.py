import django
from django.apps import apps
from ...core.functions import extract_data, chunks
from ...core.output import writeCSV
from ..functions import count_data_points
from datetime import datetime, timedelta
# from multiprocessing import Pool, cpu_count
from timeit import default_timer as timer
import pandas as pd
import numpy as np
import json
import sys
import os
from dotenv import load_dotenv
load_dotenv()
django.setup()

FILES = "lab/correlations/output/files"
JSON = "lab/correlations/output/json/correlations.json"
CSV = "lab/correlations/output/csv"

HistoricalPrices = apps.get_model('database', 'HistoricalPrices')
histprices = HistoricalPrices.objects.all()
blacklist = ['GCOW', 'FAAR']
results = {}
resultslist = []


def correct_lengths(h1, h2):
    objs = [h1.prices, h2.prices]
    smallest = [k for k, v in enumerate(objs) if len(v) == min([len(h1.prices), len(h2.prices)])][0]
    smol = objs.pop(smallest)
    big = objs[0]

    trimmedY = big[-len(smol):]

    x = extract_data(smol, 'close')
    y = extract_data(trimmedY, 'close')
    return x, y


def test_dict(results):
    start = timer()



def run_correlation(h1):
    start = timer()
    for h2 in histprices:
        comparison = "{}/{}".format(h1.stock.ticker,h2.stock.ticker)        
        if (comparison not in results):
            if (h1 != h2):
                if (h2.stock.ticker not in blacklist):
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
                    dpoints = min([h1.datapoints, h2.datapoints])
                    result = [                        
                        
                    ]
                    results[comparison] = [rv, dpoints]
                    resultslist.append([comparison, rv, dpoints])
    end = timer()
    print("Time elapsed:", end - start, "seconds")


def scanner(output="json"):
    print('Running...')
    for hp in histprices:
        if (hp.stock.ticker in blacklist):
            continue
        print("Mass Correlating: {}".format(hp.stock.ticker))
        run_correlation(hp)
