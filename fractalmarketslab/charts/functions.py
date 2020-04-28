# Functions for manipulating data


def extract_data(data, key):
    values = []
    for i, row in data.items():
        value = float(row[key])
        values.append(value)        

    return values
