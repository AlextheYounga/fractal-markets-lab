import csv
import statistics
from scipy import stats
import math
from .functions import *

# Arbitrary fractal scales
scales = {
    '1': 15821,
    '2': 7911,
    '4': 3955,
    '8': 1978,
    '16': 989,
    '32': 494,
}

# Parsing csv data
with open('fractalmarketslab/imports/RescaleRangeSPXExample.csv', newline='', encoding='utf-8') as csvfile:
    rangeData = {}
    reader = csv.DictReader(csvfile)

    for i, row in enumerate(reader):
        # Using powers of 2
        rows = {
            'date': row['\ufeffDate'] if row['\ufeffDate'] else '',
            'close': row['Close'] if row['Close'] else 0,
            'returns': row['Returns'] if row['Returns'] else 0,
        }
        # Append value dictionary to data
        rangeData[i] = rows

        # Loop through scales and append scale values to data
        rangeData[i]['stats'] = {}
        for scale, cells in scales.items():
            rangeData[i]['stats'][scale] = {}
            rangeData[i]['stats'][scale]['deviation'] = float(row['1to{}'.format(scale)]) if row['1to{}'.format(scale)] else 0
            rangeData[i]['stats'][scale]['runningTotal'] = float(row['Running Total({})'.format(scale)]) if row['Running Total({})'.format(scale)] else 0


# Collecting all returns
returns = extractData(rangeData, 'returns')

# Calculating statistics of returns and running totals
rangeStats = {}
for scale, cells in scales.items():
    runningTotals = extractData(rangeData, ['stats', scale, 'runningTotal'])
    rangeStats[scale] = {}
    rangeStats[scale]['means'] = chunkedAverages(returns, cells)
    rangeStats[scale]['stDevs'] = chunkedDevs(returns, cells)
    rangeStats[scale]['minimums'] = chunkedRange(runningTotals, cells)['minimum']
    rangeStats[scale]['maximums'] = chunkedRange(runningTotals, cells)['maximum']
    rangeStats[scale]['ranges'] = chunkedRange(runningTotals, cells)['range']


# Calculating Rescale Range
for scale, values in rangeStats.items():

    for i, value in values['ranges'].items():
        rescaleRange = (value / values['stDevs'][i] if (values['stDevs'][i] != 0) else 0)

        rangeStats[scale] = {
            'rescaleRanges': {
                i: rescaleRange,
            }
        }

# Range Analysis
for scale, values in rangeStats.items():
    rangeStats[scale]['analysis'] = {}
    rescaleRanges = extractIndexedData(values['rescaleRanges'])
    rangeStats[scale]['analysis']['rescaleRangeAvg'] = statistics.mean(rescaleRanges)
    rangeStats[scale]['analysis']['size'] = scales[scale]
    rangeStats[scale]['analysis']['rrLog'] = math.log10(statistics.mean(rescaleRanges)) if (statistics.mean(rescaleRanges) > 0) else 0
    rangeStats[scale]['analysis']['sizeLog'] = math.log10(scales[scale])

# Hurst Exponent Calculations

fractalStats = {}
# Adding rescale ranges to final data
for scale, cells in scales.items():
    fractalStats['rescaleRange'] = {
        scale: rangeStats[scale]['analysis']['rescaleRangeAvg'],
    }

# Calculating linear regression of rescale range logs
logRR = scaledDataCollector(scales, rangeStats, ['analysis', 'rrLog'])
logScales = scaledDataCollector(scales, rangeStats, ['analysis', 'sizeLog'])
slope, intercept, r_value, p_value, std_err = stats.linregress(logScales, logRR)

# Results
fractalStats['regressionResults'] = fractalCalculator(logScales, logRR)
done = True



