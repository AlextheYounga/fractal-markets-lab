import csv
import statistics
from .functions import *

scales = {
    '1': 15821,
    '2': 7911,
    '4': 3955,
    '8': 1978,
    '16': 989,
    '32': 494,
}

with open('fractalmarketslab/imports/RescaleRangeSPXExample.csv', newline='', encoding='utf-8') as csvfile:
    rangeData = {}
    reader = csv.DictReader(csvfile)

    for i, row in enumerate(reader):
        # Using powers of 2
        values = {
            'date': row['\ufeffDate'] if row['\ufeffDate'] else '',
            'close': row['Close'] if row['Close'] else 0,
            'returns': row['Returns'] if row['Returns'] else 0,
        }
        # Append value dictionary to data
        rangeData[i] = values

        # Loop through scales and append scale values to data
        rangeData[i]['stats'] = {}
        for scale, cells in scales.items():
            rangeData[i]['stats'][scale] = {}
            rangeData[i]['stats'][scale]['deviation'] = float(
                row['1to{}'.format(scale)]) if row['1to{}'.format(scale)] else 0
            rangeData[i]['stats'][scale]['runningTotal'] = float(
                row['Running Total({})'.format(scale)]) if row['Running Total({})'.format(scale)] else 0



returns = extract_data(rangeData, 'returns')

runningTotals = {}
for scale, cells in scales.items():
    runningTotals[scale] = extract_data(rangeData, ['stats', scale, 'runningTotal'])

rangeStats = {}
for scale, cells in scales.items():
    rangeStats[scale] = {}
    rangeStats[scale]['means'] = chunkedAverages(returns, cells)
    rangeStats[scale]['stDev'] = chunkedDevs(returns, cells)
    rangeStats[scale]['minimum'] = chunkedRange(runningTotals[scale], cells)['minimum']
    rangeStats[scale]['maximum'] = chunkedRange(runningTotals[scale], cells)['maximum']
    rangeStats[scale]['range'] = chunkedRange(runningTotals[scale], cells)['range']
