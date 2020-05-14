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
    if (type(scales) == list):
        if (type(key) == list):
            if len(key) == 2:
                for scale in scales:
                    value = float(data[scale][key[0]][key[1]])
                    values.append(value)
            if len(key) == 3:
                for scale in scales:
                    value = float(data[scale][key[0]][key[1]][key[2]])
                    values.append(value)
            if len(key) == 4:
                for scale in scales:
                    value = float(data[scale][key[0]][key[1]][key[2]][key[3]])
                    values.append(value)
            if len(key) > 4:
                return 'Nest level too deep to retrieve via function.'
        else:
            for scale in scales:
                value = float(data[scale][key])
                values.append(value)
                
    else:
        if (type(key) == list):
            if len(key) == 2:
                for scale, days in scales.items():
                    value = float(data[scale][key[0]][key[1]])
                    values.append(value)
            if len(key) == 3:
                for scale, days in scales.items():
                    value = float(data[scale][key[0]][key[1]][key[2]])
                    values.append(value)
            if len(key) == 4:
                for scale, days in scales.items():
                    value = float(data[scale][key[0]][key[1]][key[2]][key[3]])
                    values.append(value)
            if len(key) > 4:
                return 'Nest level too deep to retrieve via function.'
        else:
            for scale, days in scales.items():
                value = float(data[scale][key])
                values.append(value)
        
    return values


# Scale Calculators
# The function will create exponential scales, multiplying the denominator by a multiple each loop.
# The limit param will define how many loops the function runs, for how many scales the user wants.
def exponentialScales(count, multiple, limit):
    m = multiple
    itr = []
    scales = {}
    for i in range(limit):
        if (i == 0):
            scales[i + 1] = count
            itr.append(i + 1)
        else:    
            scales[(itr[i - 1] * m)] = int(count / (itr[i - 1] * m))
            itr.append(itr[i - 1] * m)

    return scales

# The function will create linear scales, adding a number on each loop.
# The limit param will define how many loops the function runs.
def linearScales(count, add, limit):
    x = add
    itr = []
    scales = {}
    for i in range(limit):
        if (i == 0):
            scales[i + 1] = count
            itr.append(i + 1)
        else:    
            scales[(itr[i - 1] + x)] = int(count / (itr[i - 1] + x))
            itr.append(itr[i - 1] + x)

    return scales
    

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
    averages = {}
    for i, chunk in enumerate(chunkedList):
        mean = statistics.mean(chunk)
        averages[i] = mean

    return averages


def deviationsCalculator(returns, scales):
    deviations = {}
    for scale, days in scales.items():
        deviations[scale] = []
        chunkedReturns = chunks(returns, days)
        chunkedMeans = chunkedAverages(returns, days)
        for index, chunk in enumerate(chunkedReturns):
            for i, value in enumerate(chunk):
                deviation = float(value) - float(chunkedMeans[index])
                deviations[scale].append(deviation)
    return deviations


def runningTotalsCalculator(deviations, scales):
    runningTotals = {}
    for scale, days in scales.items():
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
