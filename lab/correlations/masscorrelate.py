import django
from django.apps import apps
from ..core.functions import extract_data, chunks
from datetime import datetime, timedelta
from multiprocessing import Pool, cpu_count
import numpy as np
import json
import sys
import os
from dotenv import load_dotenv
from ..twitter.tweet import send_tweet
load_dotenv()
django.setup()
OUTPUT = "lab/correlations/output/"


def start_process(chunk):
    def scan_output_folder():
        files = os.listdir(OUTPUT)
        return [f.split('.').pop(0) for f in files]

    def correct_lengths(h1, h2):
        objs = [h1.prices, h2.prices]
        smallest = [k for k, v in enumerate(objs) if len(v) == min([len(h1.prices), len(h2.prices)])][0]
        smol = objs.pop(smallest)
        big = objs[0]
        
        trimmedY = big[-len(smol):]

        x = extract_data(smol.prices, 'close')
        y = extract_data(trimmedY, 'close')
        return x, y

    def run_correlation(h1):
        correlations = []
        
        for h2 in priceobjs:
            if h1 == h2: continue
            if (h2.stock.ticker in badset): continue
            
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
            result = {'comparand': h2.stock.ticker, 'rvalue': rv}
            correlations.append(result)
        with open('{}.txt'.format(OUTPUT + h1.stock.ticker), 'w') as txtfile:
            json.dump(correlations, txtfile)

    for h in chunk:
        if (h.stock.ticker in scan_output_folder()): continue
        if (h.stock.ticker in badset): continue
        print("Mass Correlating: {}".format(h.stock.ticker))
        run_correlation(h)


HistoricalPrices = apps.get_model('database', 'HistoricalPrices')
priceobjs = HistoricalPrices.objects.all()
badset = ['GCOW', 'FAAR']
if __name__ == '__main__':
    print('Running...')
    chunk_count = int(len(priceobjs) / (int(cpu_count() / 2)))
    chunkobjs = chunks(priceobjs, chunk_count)
    for chunk in chunkobjs:
        p = Pool(int(cpu_count() / 2))
        p.apply_async(start_process, args=(chunk,))
