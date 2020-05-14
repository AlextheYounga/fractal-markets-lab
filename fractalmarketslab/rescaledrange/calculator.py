import csv
import statistics
from scipy import stats
import math
from .functions import *
from .export import exportFractal
import sys


# Parsing csv data
with open('fractalmarketslab/imports/currentSPX.csv', newline='', encoding='utf-8') as csvfile:
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

# Arbitrary fractal scales
count = len(prices)

scales = exponentialScales(count, 3, 6)

print(json.dumps(scales, indent=1))

returns = returnsCalculator(prices)
deviations = deviationsCalculator(returns, scales)
runningTotals = runningTotalsCalculator(deviations, scales)

# Calculating statistics of returns and running totals
rangeStats = {}
for scale, days in scales.items():
    rangeStats[scale] = {}
    rangeStats[scale]['means'] = chunkedAverages(returns, days)
    rangeStats[scale]['stDevs'] = chunkedDevs(returns, days)
    rangeStats[scale]['minimums'] = chunkedRange(runningTotals[scale], days)['minimum']
    rangeStats[scale]['maximums'] = chunkedRange(runningTotals[scale], days)['maximum']
    rangeStats[scale]['ranges'] = chunkedRange(runningTotals[scale], days)['range']


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
for scale, days in scales.items():
    fractalResults['rescaleRange'][scale] = round(rangeStats[scale]['keyStats']['rescaleRangeAvg'], 2)


# Calculating linear regression of rescale range logs
logRRs = scaledDataCollector(scales, rangeStats, ['keyStats', 'logRR'])
logScales = scaledDataCollector(scales, rangeStats, ['keyStats', 'logScale'])
slope, intercept, r_value, p_value, std_err = stats.linregress(logScales, logRRs)

# Calculator
def fractalSections(x, y):
    if len(x) != len(y):
        return "X and Y values contain disproportionate counts"

    fractalScales = {
        'trade': {
            'x': list(backwardChunks(x, 2))[-1],
            'y': list(backwardChunks(y, 2))[-1],
        },
        'month': {
            'x': list(backwardChunks(x, 3))[-1],
            'y': list(backwardChunks(y, 3))[-1],
        },
        'trend': {
            'x': list(backwardChunks(x, 4))[-1],
            'y': list(backwardChunks(y, 4))[-1],
        },
        'tail': {
            'x': list(backwardChunks(x, 5))[-1],
            'y': list(backwardChunks(y, 5))[-1],
        },
    }
    return fractalScales


def fractalCalculator(x, y):
    sections = fractalSections(x, y)
    results = {}
    for i, section in sections.items():
        slope, intercept, r_value, p_value, std_err = stats.linregress(section['x'], section['y'])
        results[i] = {
            'hurstExponent': round(slope, 2),
            'fractalDimension': round((2 - slope), 2),
            'r-squared': round(r_value**2, 2),
            'p-value': round(p_value, 2),
            'standardError': round(std_err, 2)
        }
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    results['fullSeries'] = {
        'hurstExponent': round(slope, 2),
        'fractalDimension': round((2 - slope), 2),
        'r-squared': round(r_value**2, 2),
        'p-value': round(p_value, 2),
        'standardError': round(std_err, 2)
    }
    return results


# Results
fractalResults['regressionResults'] = fractalCalculator(logScales, logRRs)
# print(json.dumps(fractalResults, indent=1))

# Export to CSV
exportFractal(fractalResults, scales)
