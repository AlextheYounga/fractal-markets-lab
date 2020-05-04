import csv
import statistics
import math
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
            rangeData[i]['stats'][scale]['deviation'] = float(row['1to{}'.format(scale)]) if row['1to{}'.format(scale)] else 0
            rangeData[i]['stats'][scale]['runningTotal'] = float(row['Running Total({})'.format(scale)]) if row['Running Total({})'.format(scale)] else 0


returns = extractData(rangeData, 'returns')

runningTotals = {}
for scale, cells in scales.items():
    runningTotals[scale] = extractData(rangeData, ['stats', scale, 'runningTotal'])

rangeStats = {}
for scale, cells in scales.items():
    rangeStats[scale] = {}
    rangeStats[scale]['means'] = chunkedAverages(returns, cells)
    rangeStats[scale]['stDevs'] = chunkedDevs(returns, cells)
    rangeStats[scale]['minimums'] = chunkedRange(runningTotals[scale], cells)['minimum']
    rangeStats[scale]['maximums'] = chunkedRange(runningTotals[scale], cells)['maximum']
    rangeStats[scale]['ranges'] = chunkedRange(runningTotals[scale], cells)['range']


# Calculating Rescale Range
for scale, stats in rangeStats.items():
    rangeStats[scale]['rescaleRanges'] = {}

    for i, value in stats['ranges'].items():
        rescaleRange = (value / stats['stDevs'][i] if (stats['stDevs'][i] != 0) else 0)
        rangeStats[scale]['rescaleRanges'][i] = rescaleRange

# Range Analysis
for scale, stats in rangeStats.items():
    rangeStats[scale]['analysis'] = {}
    rescaleRanges = extractIndexedData(stats['rescaleRanges'])
    
    rangeStats[scale]['analysis']['rescaleRangeAvg'] = statistics.mean(rescaleRanges)
    rangeStats[scale]['analysis']['size'] = scales[scale]
    rangeStats[scale]['analysis']['rrAvgLog'] = math.log10(statistics.mean(rescaleRanges)) if (statistics.mean(rescaleRanges) > 0) else 0
    rangeStats[scale]['analysis']['sizeLog'] = math.log10(scales[scale])
