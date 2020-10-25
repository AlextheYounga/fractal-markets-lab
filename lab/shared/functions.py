import sys
import statistics
import math
import pandas as pd
import numpy as np
# Returns a list of items from a nested object.


def extractData(data, key):
    values = []
    if (type(key) == list):
        if len(key) == 2:
            for i, row in data.items():
                value = row[key[0]][key[1]]
                values.append(value)
        if len(key) == 3:
            for i, row in data.items():
                value = row[key[0]][key[1]][key[2]]
                values.append(value)
        if len(key) == 4:
            for i, row in data.items():
                value = row[key[0]][key[1]][key[2]][key[3]]
                values.append(value)
        if len(key) == 5:
            for i, row in data.items():
                value = row[key[0]][key[1]][key[2]][key[3]][key[4]]
                values.append(value)
        if len(key) > 5:
            return 'Nest level too deep to retrieve via function.'
    else:
        for i, row in data.items():
            value = row[key]
            values.append(value)
    return values

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def removeZeroes(lst):
    while 0 in lst:
        lst.remove(0)
    while 0.0 in lst:
        lst.remove(0.0)
    return lst


def logReturns(prices):
    series = pd.Series(prices)
    log_returns = (np.log(series) - np.log(series.shift(1))).dropna()

    return list(log_returns)

def calculateVol(prices):
    stdevTrade = statistics.stdev(prices[:16])
    stdevMonth = statistics.stdev(prices[:22])
    stdevTrend = statistics.stdev(prices[:64])    
    volTrade = prices[-1] * (stdevTrade / prices[-1]) * (math.sqrt(1/16)) if (prices[-1] != 0) else 0
    volMonth = prices[-1] * (stdevMonth / prices[-1]) * (math.sqrt(1/22)) if (prices[-1] != 0) else 0
    volTrend = prices[-1] * (stdevTrend / prices[-1]) * (math.sqrt(1/64)) if (prices[-1] != 0) else 0
    volMean = round(statistics.mean([volTrade, volMonth, volTrend]), 3)

    return volMean
    
