import csv
import os
from .functions import *
from datetime import datetime


def exportFractal(fractalResults):
    now = datetime.now()
    datenow = now.strftime("%m%d%Y%H%M%S")
    output_file = 'fractalmarketslab/exports/regression/regression_results.csv'

    if os.path.exists(output_file):
        os.remove(output_file)

    with open(output_file, mode='w') as regressionfile:
        write_regression = csv.writer(regressionfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        results_scales = []
        headers = []
        for scale, stats in fractalResults['regressionResults'].items():
            results_scales.append(scale)
        for header, value in fractalResults['regressionResults'][results_scales[0]].items():
            headers.append(header)
        
        # Making lists from each set of data
        hurstExponents = scaledDataCollector(results_scales, fractalResults['regressionResults'],'hurstExponent')
        fractalDimensions = scaledDataCollector(results_scales, fractalResults['regressionResults'],'fractalDimension')
        rSquared = scaledDataCollector(results_scales, fractalResults['regressionResults'],'r-squared')
        pValues = scaledDataCollector(results_scales, fractalResults['regressionResults'],'p-value')
        standardErrors = scaledDataCollector(results_scales, fractalResults['regressionResults'],'standardError')
        # Zipping all lists into row
        rows = zip(results_scales, hurstExponents, fractalDimensions, rSquared, pValues, standardErrors)

        # Headers
        headers.insert(0, '')
        write_regression.writerow(headers)

        # Columns
        for row in rows:
            write_regression.writerow(row)
