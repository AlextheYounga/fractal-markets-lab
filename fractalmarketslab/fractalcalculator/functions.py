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


def percentChange(lst, i):
    change = {
        'dayChange': (lst[i] - lst[i + 1]) / lst[i + 1] if (i + 1 in range(-len(lst), len(lst)) and lst[i + 1] != 0) else 0,
        'trade': (lst[i] - lst[i + 16]) / lst[i + 16] if (i + 16 in range(-len(lst), len(lst)) and lst[i + 16] != 0) else 0,
        'trend': (lst[i] - lst[i + 64]) / lst[i + 64] if (i + 64 in range(-len(lst), len(lst)) and lst[i + 64] != 0) else 0,
        'tail': (lst[i] - lst[i + 757]) / lst[i + 757] if (i + 757 in range(-len(lst), len(lst)) and lst[i + 757] != 0) else 0,
    }
    return change


def returnsCalculator(prices):
    returns = []
    for i, price in enumerate(prices):
        return_value = (price / float(prices[i + 1]) - 1) if (i + 1 in range(-len(prices), len(prices)) and float(prices[i + 1]) != 0) else 0
        returns.append(return_value)
    return returns


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


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


# Test Function
def fractalSections(x, y):
    if len(x) != len(y):
        return "X and Y values contain disproportionate counts"

    half = int(len(x) / 2)
    third = int(len(x) / 3)

    fractalScales = {
        'pastHalfSeries': {
            'x': list(chunks(x, half))[0],
            'y': list(chunks(y, half))[0]
        },
        'currentHalfSeries': {
            'x': list(chunks(x, half))[1],
            'y': list(chunks(y, half))[1]
        },
        'pastThirdSeries': {
            'x': list(chunks(x, third))[0],
            'y': list(chunks(y, third))[0]
        },
        'middleThirdSeries': {
            'x': list(chunks(x, third))[1],
            'y': list(chunks(y, third))[1]
        },
        'currentThirdSeries': {
            'x': list(chunks(x, third))[2],
            'y': list(chunks(y, third))[2]
        },
    }
    return fractalScales


def fractalCalculator(x, y):
    sections = fractalSections(x, y)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    results = {
        'fullSeries': {
            'hurstExponent': slope,
            'fractalDimension': 2 - slope,
            'r-squared': r_value**2,
            'p-value': p_value,
            'standardError': std_err
        },
    }

    for i, section in sections.items():
        slope, intercept, r_value, p_value, std_err = stats.linregress(section['x'], section['y'])
        results[i] = {
            'hurstExponent': slope,
            'fractalDimension': 2 - slope,
            'r-squared': r_value**2,
            'p-value': p_value,
            'standardError': std_err
        }
    return results
