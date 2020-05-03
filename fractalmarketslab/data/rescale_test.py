import csv
import statistics
from .functions import *

with open('fractalmarketslab/imports/RescaleRangeSPXExample.csv', newline='', encoding='utf-8') as csvfile:
    rangeData = {}
    reader = csv.DictReader(csvfile)

    
    for i, row in enumerate(reader):
        # Using powers of 2
        values = {
            'date': row['\ufeffDate'] if row['\ufeffDate'] else '',
            'close': row['Close'] if row['Close'] else 0,
            'returns': row['Returns'] if row['Returns'] else 0,

            'stats': {
                '1': {
                    'deviation': row['1to1'] if row['1to1'] else 0,
                    'runningTotal': row['Running Total(1)'] if row['Running Total(1)'] else 0,
                },
                 '2': {
                    'deviation': row['1to2'] if row['1to2'] else 0,
                    'runningTotal': row['Running Total(2)'] if row['Running Total(2)'] else 0,
                },
                 '4': {
                    'deviation': row['1to4'] if row['1to4'] else 0,
                    'runningTotal': row['Running Total(4)'] if row['Running Total(4)'] else 0,
                },
                 '8': {
                    'deviation': row['1to8'] if row['1to8'] else 0,
                    'runningTotal': row['Running Total(8)'] if row['Running Total(8)'] else 0,
                },
                 '16': {
                    'deviation': row['1to16'] if row['1to16'] else 0,
                    'runningTotal': row['Running Total(16)'] if row['Running Total(16)'] else 0,
                },
                 '32': {
                    'deviation': row['1to32'] if row['1to32'] else 0,
                    'runningTotal': row['Running Total(32)'] if row['Running Total(32)'] else 0,
                },
            }
        }

        # Append value dictionary to data
        rangeData[i] = values

scales = {
    '1': 15821,
    '2': 7911,
    '4': 3955,
    '8': 1978,
    '16': 989,
    '32': 494,

}

returns = extract_data(rangeData, 'returns')

rangeStats = {
    '1': {
        'means': chunkedAverages(returns, scales['1']),
        'stDev': chunkedDevs(returns, scales['1']),
    },
    '2': {
        'means': chunkedAverages(returns, scales['2']),
        'stDev': chunkedDevs(returns, scales['2']),
    },
    '4': {
        'means': chunkedAverages(returns, scales['4']),
        'stDev': chunkedDevs(returns, scales['4']),
    },
    '8': {
        'means': chunkedAverages(returns, scales['8']),
        'stDev': chunkedDevs(returns, scales['8']),
    },
    '16': {
        'means': chunkedAverages(returns, scales['16']),
        'stDev': chunkedDevs(returns, scales['16']),
    },
    '32': {
        'means': chunkedAverages(returns, scales['32']),
        'stDev': chunkedDevs(returns, scales['32']),
    },
}


