# Functions for manipulating data


def extract_data(data, key):
    values = []
    for i, row in data.items():
        value = float(row[key])
        values.append(value)        

    return values

def percentChange(list, i):
    change = {
        'dayChange': (list[i] - list[i + 1]) / list[i + 1] if  list[i + 1] else 0,
        'trade': (list[i] - list[i + 16]) / list[i + 16] if  list[i + 16] else 0,
        'trend': (list[i] - list[i + 64]) / list[i + 64] if  list[i + 64] else 0,
        'tail': (list[i] - list[i + 757]) / list[i + 757] if  list[i + 757] else 0,
    }
    return change

    