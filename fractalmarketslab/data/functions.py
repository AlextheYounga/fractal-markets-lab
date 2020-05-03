import json
import statistics 
# Functions for manipulating data


def extract_data(data, key):
    values = []
    for i, row in data.items():
        value = float(row[key])
        values.append(value)        

    return values

def percentChange(lst, i):
    change = {
        'dayChange': (lst[i] - lst[i + 1]) / lst[i + 1] if  (i + 1 in range(-len(lst), len(lst)) and lst[i + 1] != 0) else 0,
        'trade': (lst[i] - lst[i + 16]) / lst[i + 16] if  (i + 16 in range(-len(lst), len(lst)) and lst[i + 16] != 0) else 0,
        'trend': (lst[i] - lst[i + 64]) / lst[i + 64] if  (i + 64 in range(-len(lst), len(lst)) and lst[i + 64] != 0) else 0,
        'tail': (lst[i] - lst[i + 757]) / lst[i + 757] if  (i + 757 in range(-len(lst), len(lst)) and lst[i + 757] != 0) else 0,
    }
    return change

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def chunkedAverages(lst, n):
    chunkedList = list(chunks(lst, n))
    averages = {}
    for i, chunk in enumerate(chunkedList):
        mean = statistics.mean(chunk)
        formattedMean = format(mean, ".2%")        
        averages[i] = formattedMean
    
    return averages

def chunkedDevs(lst, n):
    chunkedList = list(chunks(lst, n))
    stDevs = {}
    for i, chunk in enumerate(chunkedList):
        if (len(chunk) > 1):
            dev = statistics.stdev(chunk)
            formattedDev = format(dev, ".2%")
            stDevs[i] = formattedDev
        else:
            stDevs[i] = 0
    
    return stDevs
        
    