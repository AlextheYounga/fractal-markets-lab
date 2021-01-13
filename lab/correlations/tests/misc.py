import time
from multiprocessing import Pool
import django
from django.apps import apps
import multiprocessing as mp
from multiprocessing import Process
from ..core.functions import extract_data, chunks
from datetime import datetime, timedelta
import numpy as np
import json
import sys
import os
from dotenv import load_dotenv
from ..fintwit.tweet import send_tweet
load_dotenv()
django.setup()
# OUTPUT = "lab/correlations/output/"


HistoricalPrices = apps.get_model('database', 'HistoricalPrices')
priceobjs = HistoricalPrices.objects.all()

bad_data = []
def compare(h1):
    for h2 in priceobjs:
        if (h1.stock.ticker == h2.stock.ticker): continue
        if (len(h1.prices) == len(h2.prices)): continue
        objs = [h1.prices, h2.prices]
        smallest = [k for k, v in enumerate(objs) if len(v) == min([len(h1.prices), len(h2.prices)])][0]
        smol = objs.pop(smallest)
        big = objs[0]
        
        # if (big[-1]['date'] == smol[-1]['date']):
        builtY = big[-len(smol):]
        
        x = extract_data(smol, 'date')
        y = extract_data(builtY, 'date')
        datacheck = (x == y)
        if (datacheck == False):
            # print('Bad Data {}'.format(h2.stock.ticker))
            bad_data.append(h2.stock.ticker)


        # matchedY = []
        # for item in smol:
        #     for day in big:
        #         if (item['date'] == day['date']):
        #             matchedY.append(day)


for h in priceobjs:
    bad = ['GCOW', 'FAAR']
    if (h.stock.ticker in bad): continue
    #     print(extract_data(h.prices, 'date'))
    #     sys.exit()
    print(h.stock.ticker)
    compare(h)

if (bad_data):
    badset = set(bad_data)
    print(list(badset))
