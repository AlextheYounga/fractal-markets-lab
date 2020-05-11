import csv
import statistics
from scipy import stats
import math
from .functions import *
import sys

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
    assetData = {}
    reader = csv.DictReader(csvfile)

    for i, row in enumerate(reader):
        # Using powers of 2
        rows = {
            'date': row['\ufeffDate'] if row['\ufeffDate'] else '',
            'close': row['Close'] if row['Close'] else 0
        }
        # Append value dictionary to data
        assetData[i] = rows


prices = extractData(assetData, 'close')
returns = returnsCalculator(prices)
deviations = deviationsCalculator(returns, scales)
runningTotals = runningTotalsCalculator(deviations, scales)

# Calculating statistics of returns and running totals
rangeStats = {}
for scale, cells in scales.items():    
    rangeStats[scale] = {}
    rangeStats[scale]['means'] = chunkedAverages(returns, cells)
    rangeStats[scale]['stDevs'] = chunkedDevs(returns, cells)
    rangeStats[scale]['minimums'] = chunkedRange(runningTotals[scale], cells)['minimum']
    rangeStats[scale]['maximums'] = chunkedRange(runningTotals[scale], cells)['maximum']
    rangeStats[scale]['ranges'] = chunkedRange(runningTotals[scale], cells)['range']


# Calculating Rescale Range
for scale, values in rangeStats.items():
    rangeStats[scale]['rescaleRanges'] = {}
    for i, value in values['ranges'].items():
        rescaleRange = (value / values['stDevs'][i] if (values['stDevs'][i] != 0) else 0)

        rangeStats[scale]['rescaleRanges'][i] = rescaleRange

# Key stats for fractal calculations
for scale, values in rangeStats.items():
    rangeStats[scale]['keyStats'] = {}
    rescaleRanges = list(values['rescaleRanges'].values())
    rangeStats[scale]['keyStats']['rescaleRangeAvg'] = statistics.mean(rescaleRanges)
    rangeStats[scale]['keyStats']['size'] = scales[scale]
    rangeStats[scale]['keyStats']['logRR'] = math.log10(statistics.mean(rescaleRanges)) if (statistics.mean(rescaleRanges) > 0) else 0
    rangeStats[scale]['keyStats']['logScale'] = math.log10(scales[scale])

# Hurst Exponent Calculations
fractalResults = {
    'rescaleRange': {}
}
# Adding rescale ranges to final data
for scale, cells in scales.items():
    fractalResults['rescaleRange'][scale] = rangeStats[scale]['keyStats']['rescaleRangeAvg']

# Calculating linear regression of rescale range logs
logRRs = scaledDataCollector(scales, rangeStats, ['keyStats', 'logRR'])
logScales = scaledDataCollector(scales, rangeStats, ['keyStats', 'logScale'])
slope, intercept, r_value, p_value, std_err = stats.linregress(logScales, logRRs)

# Calculator
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

# Results
fractalResults['regressionResults'] = fractalCalculator(logScales, logRRs)
done = True
