import json
import statistics
from scipy import stats
# Functions for manipulating data


# Returns a list of items from a nested object.
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

# Returns a list of data from a nested object that contains specific scales
def scaledDataCollector(scales, data, key):
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

# Creates a list of returns from a list of prices.
def returnsCalculator(prices):
    returns = []
    for i, price in enumerate(prices):
        return_value = (price / float(prices[i + 1]) - 1) if (i + 1 in range(-len(prices), len(prices)) and float(prices[i + 1]) != 0) else 0
        returns.append(return_value)
    return returns

# Returns chunked lists
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def backwardChunks(lst, n):
    start = 0
    for end in range(len(lst)%n, len(lst)+1, n):
        yield lst[start:end]
        start = end


# Formulas for chunking data into the different scales (i.e. 1:1, 1:2, 1:4, ... 1:32)
def chunkedAverages(lst, n):
    chunkedList = list(chunks(lst, n))
    # if (len(chunkedList[-1]) == 1):
    #     remainder = chunkedList[-1].pop(0)
    #     chunkedList[-2].append(remainder)
    #     del chunkedList[-1]
    averages = {}
    for i, chunk in enumerate(chunkedList):
        mean = statistics.mean(chunk)
        averages[i] = mean

    return averages


def deviationsCalculator(returns, scales):
    deviations = {}
    for scale, cells in scales.items():
        deviations[scale] = []
        chunkedReturns = chunks(returns, cells)
        chunkedMeans = chunkedAverages(returns, cells)
        for index, chunk in enumerate(chunkedReturns):
            for i, value in enumerate(chunk):
                deviation = float(value) - float(chunkedMeans[index])
                deviations[scale].append(deviation)
    return deviations


def runningTotalsCalculator(deviations, scales):
    runningTotals = {}
    for scale, cells in scales.items():
        runningTotals[scale] = []
        for i, value in enumerate(deviations[scale]):
            if (i == 0):
                runningTotals[scale].append(value)
                continue
            rt = value + runningTotals[scale][i - 1]
            runningTotals[scale].append(rt)
    return runningTotals


def chunkedDevs(lst, n):
    chunkedList = list(chunks(lst, n))
    # if (len(chunkedList[-1]) == 1):
    #     remainder = chunkedList[-1].pop(0)
    #     chunkedList[-2].append(remainder)
    #     del chunkedList[-1]
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
    if (len(chunkedList[-1]) == 1):
        remainder = chunkedList[-1].pop(0)
        chunkedList[-2].append(remainder)
        del chunkedList[-1]
    chunkRange = {}
    chunkRange['minimum'] = {}
    chunkRange['maximum'] = {}
    chunkRange['range'] = {}
    for i, chunk in enumerate(chunkedList):
        chunkRange['minimum'][i] = min(chunk)
        chunkRange['maximum'][i] = max(chunk)
        chunkRange['range'][i] = (max(chunk) - min(chunk))

    return chunkRange
