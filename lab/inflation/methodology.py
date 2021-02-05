from dotenv import load_dotenv
import pandas as pd
import numpy as np
import redis
import statistics
import json
import sys
from datetime import date
from ..redisdb.controller import update_prices
from ..core.functions import chunks
from ..core.api import quoteStatsBatchRequest, getStockInfo
from ..core.output import printFullTable, writeCSV
load_dotenv()


def sectors():
    return [
        'XLY',
        'XLP',
        'XLE',
        'XLF',
        'XLV',
        'XLI',
        'XLB',
        'XLK',
        'IXP',
        'USRT',
        'XLU',
        'XME',
        'VNQ',
        'GDX',
        'AMLP',
        'ITB',
        'OIH',
        'KRE',
        'XRT',
        'MOO',
        'FDN',
        'IBB',
        'SMH',
        'XOP',
        'PBW',
        'KIE',
        'PHO',
        'IGV'
        # 'XLC',
        # 'IYR',
        # 'XLRE',
    ]


def trim_data(data):
    trimmed = {}
    COUNT = len(sectors())
    for date, prices in data.items():
        if (len(prices) != COUNT):
            continue
        trimmed[date] = prices

    return trimmed


def formula(data):
    avgs = {}
    for day, prices in data.items():
        avg = statistics.mean(prices)
        avgs[day] = avg
    

    return avgs


def calculate(update):
    r = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)
    data = {}

    for ticker in sectors():
        print(ticker)
        if (update):
            update_prices(ticker)

        prices = json.loads(r.get('stock-'+ticker+'-prices'))

        if (prices):

            for row in prices:
                if (row['date'] not in data):
                    data[row['date']] = []

                data[row['date']].append(float(row['close']))

    data = trim_data(data)

    return formula(data) if (data) else "Unexpected Error"
