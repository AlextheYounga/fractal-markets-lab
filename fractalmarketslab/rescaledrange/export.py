import csv
import os
from .functions import *
from datetime import datetime


def exportFractal(fractalResults):
    now = datetime.now()
    datenow = now.strftime("%m%d%Y%H%M%S")
    output_file = 'fractalmarketslab/exports/fractal_results.csv'

    if os.path.exists(output_file):
        os.remove(output_file)

    with open(output_file, mode='w') as resultsfile:
        write_results = csv.writer(resultsfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        write_results.writerow(['Fractal Statistics:'])

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

        # Writing Headers
        headers.insert(0, '')
        write_results.writerow(headers)

        # Writing Data Columns
        for row in rows:
            write_results.writerow(row)

        # Rescale Range
        write_results.writerow('')
        write_results.writerow(['Rescale Range:'])
        write_results.writerow(['Scale', 'RescaleRange'])
        for scale, rr in fractalResults['rescaleRange'].items():
            write_results.writerow(['fullSeries / {}'.format(scale), rr])


