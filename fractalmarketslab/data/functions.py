import json
import statistics
from scipy import stats
# Functions for manipulating data


def extractData(data, key):
    values = []
    if (type(key) == list):
        if len(key) == 2:
            for i, row in data.items():
                value = float(row[key[0]][key[1]])
                values.append(value)
        if len(key) == 3:
            for i, row in data.items():
                value = float(row[key[0]][key[1]][key[2]])
                values.append(value)
        if len(key) == 4:
            for i, row in data.items():
                value = float(row[key[0]][key[1]][key[2]][key[3]])
                values.append(value)
        if len(key) == 5:
            for i, row in data.items():
                value = float(row[key[0]][key[1]][key[2]][key[3]][key[4]])
                values.append(value)
        if len(key) > 5:
            return 'Nest level too deep to retrieve via function.'
    else:
        for i, row in data.items():
            value = float(row[key])
            values.append(value)
    return values


def extractIndexedData(data):
    values = list(data.values())
    return values


def collectScaledData(scales, data, key):
    values = []
    if (type(key) == list):
        if len(key) == 2:
            for scale, cells in scales.items():
                value = float(data[scale][key[0]][key[1]])
                values.append(value)
        if len(key) == 3:
            for scale, cells in scales.items():
                value = float(data[scale][key[0]][key[1]][key[2]])
                values.append(value)
        if len(key) == 4:
            for scale, cells in scales.items():
                value = float(data[scale][key[0]][key[1]][key[2]][key[3]])
                values.append(value)
        if len(key) > 4:
            return 'Nest level too deep to retrieve via function.'
    else:
        for scale, cells in scales.items():
            value = float(data[scale][key])
            values.append(value)
    return values


def percentChange(lst, i):
    change = {
        'dayChange': (lst[i] - lst[i + 1]) / lst[i + 1] if (i + 1 in range(-len(lst), len(lst)) and lst[i + 1] != 0) else 0,
        'trade': (lst[i] - lst[i + 16]) / lst[i + 16] if (i + 16 in range(-len(lst), len(lst)) and lst[i + 16] != 0) else 0,
        'trend': (lst[i] - lst[i + 64]) / lst[i + 64] if (i + 64 in range(-len(lst), len(lst)) and lst[i + 64] != 0) else 0,
        'tail': (lst[i] - lst[i + 757]) / lst[i + 757] if (i + 757 in range(-len(lst), len(lst)) and lst[i + 757] != 0) else 0,
    }
    return change


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


# Formulas for chunking data into the different scales (i.e. 1:1, 1:2, 1:4, ... 1:32)

def chunkedAverages(lst, n):
    chunkedList = list(chunks(lst, n))
    averages = {}
    for i, chunk in enumerate(chunkedList):
        mean = statistics.mean(chunk)
        averages[i] = mean

    return averages


def chunkedDevs(lst, n):
    chunkedList = list(chunks(lst, n))
    stDevs = {}
    for i, chunk in enumerate(chunkedList):
        # Checking if chunk is more than one item; stDev needs more than one.
        if (len(chunk) > 1):
            dev = statistics.stdev(chunk)
            stDevs[i] = dev
        else:
            stDevs[i] = 0

    return stDevs


def chunkedRange(lst, n):
    chunkedList = list(chunks(lst, n))
    chunkRange = {}
    chunkRange['minimum'] = {}
    chunkRange['maximum'] = {}
    chunkRange['range'] = {}
    for i, chunk in enumerate(chunkedList):
        chunkRange['minimum'][i] = min(chunk)
        chunkRange['maximum'][i] = max(chunk)
        chunkRange['range'][i] = (max(chunk) - min(chunk))

    return chunkRange

def calculateLineRegression(x, y):    
    line = stats.linregress(x, y)
    results = {
        'slope': line[0],
        'intercept': line[1],
        'r-value': line[2],
        'p-value': line[3],
        'standardError': line[4],
    }
    return results