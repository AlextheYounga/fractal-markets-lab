import json
# Functions for manipulating data


def extract_data(data, key):
    values = []
    for i, row in data.items():
        value = float(row[key])
        values.append(value)        

    return values

def percentChange(list, i):
    change = {
        'dayChange': (list[i] - list[i + 1]) / list[i + 1] if  (i + 1 in range(-len(list), len(list)) and list[i + 1] != 0) else 0,
        'trade': (list[i] - list[i + 16]) / list[i + 16] if  (i + 16 in range(-len(list), len(list)) and list[i + 16] != 0) else 0,
        'trend': (list[i] - list[i + 64]) / list[i + 64] if  (i + 64 in range(-len(list), len(list)) and list[i + 64] != 0) else 0,
        'tail': (list[i] - list[i + 757]) / list[i + 757] if  (i + 757 in range(-len(list), len(list)) and list[i + 757] != 0) else 0,
    }
    return change

def chunks(list, n):
    for i in range(0, len(list), n):
        yield list[i:i + n]


def chunkedAverages(list, chunk, limit):
    
    return
    