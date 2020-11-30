import django
from django.apps import apps
import multiprocessing as mp
from multiprocessing import Process
from ..core.functions import extract_data, chunks
from datetime import datetime, timedelta
from itertools import product
import numpy as np
import json
import sys
import os
from dotenv import load_dotenv
from ..twitter.tweet import send_tweet
load_dotenv()
django.setup()


def correct_lengths(h1, h2):
    objs = [h1, h2]
    smallest = [k for k, v in enumerate(objs) if len(v.prices) == min([len(h1.prices), len(h2.prices)])]
    smol = objs.pop(smallest[0])
    big = objs.pop(0)

    matchedY = []
    for item in smol.prices:
        match = [day for day in big.prices if item['date'] == day['date']][0]
        matchedY.append(match)

    x = extract_data(smol.prices, 'close')
    y = extract_data(matchedY, 'close')
    return x, y


def run_correlation(h1, stock):
    x = extract_data(h1.prices, 'close')
    for h2 in priceobjs:
        if h1 == h2:
            continue
        y = extract_data(h2.prices, 'close')
        if ((len(x) == len(y)) == False):
            x, y = correct_lengths(h1, h2)

        r = np.corrcoef(x, y)
        rv = r[0, 1]
        print("{} - {}: {}".format(h1.stock.ticker, h2.stock.ticker, rv))
        correlation, created = Correlations.objects.update_or_create(
            stock=stock, 
            comparand=h2.stock.ticker, 
            defaults={'rvalue': rv})


start = datetime.now()
Stock = apps.get_model('database', 'Stock')
HistoricalPrices = apps.get_model('database', 'HistoricalPrices')
Correlations = apps.get_model('database', 'Correlation')
priceobjs = HistoricalPrices.objects.all()


for h in priceobjs:
    stock = Stock.objects.get(ticker=h.stock.ticker)
    run_correlation(h, stock)

end = datetime.now()
runtime = (end - start).seconds
print("Time: {}".format(runtime))


# correlations = []
# def log_result(result):
    # This is called whenever foo_pool(i) returns a result.
    # result_list is modified only by the main process, not the pool workers.
    # correlations.append(result)


# def start_process(chunk, priceobjs):
#     print('Starting process...')
#     for h in chunk:
#         run_correlation(h, priceobjs)


# def apply_async_with_callback():
#     start = datetime.now()
#     HistoricalPrices = apps.get_model('database', 'HistoricalPrices')
#     priceobjs = HistoricalPrices.objects.all()
#     chunkobjs = chunks(priceobjs, (int(mp.cpu_count() / 2)))

#     for chunk in chunkobjs:
#         pool = mp.Pool(int(mp.cpu_count()/2))  # Init multiprocessing.Pool() using your computer's cpu count.
#         process = pool.apply_async(start_process, args=(chunk, priceobjs))  # adding process to pool
#         pool.close()  # closing pool

#     end = datetime.now()
#     runtime = (end - start).seconds
#     print("Time: {}".format(runtime))
    # print(len(correlations))


# if __name__ == '__main__':
#     print('Running...')
#     apply_async_with_callback()
