import csv
import os
from .functions import *
from datetime import datetime

def exportFractal(fractalResults, refScales):
    output_file = 'fractalmarketslab/exports/fractal_results.csv'
    now = datetime.now()
    datenow = now.strftime("%m-%d-%Y %H:%M:%S")

    # If output file already exists, append results, else generate new file.
    if (os.path.exists(output_file)):
        with open(output_file, mode='a') as resultsfile:
            write_results = csv.writer(resultsfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for x in range(2):
                write_results.writerow([''])

            write_results.writerow(['Fractal Statistics', 'Generated {}'.format(datenow)])

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
            headers.insert(0, 'Scale')
            write_results.writerow(headers)

            # Writing Data Columns
            for row in rows:
                write_results.writerow(row)

            # Rescale Range
            write_results.writerow('')
            write_results.writerow(['Rescale Range:'])
            write_results.writerow(['Scale', 'RescaleRange'])
            for scale, rr in fractalResults['rescaleRange'].items():
                write_results.writerow(['fullSeries / {} : {} day chunks'.format(scale, refScales[scale]), rr])

    else:
        with open(output_file, mode='w') as resultsfile:
            write_results = csv.writer(resultsfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            write_results.writerow(['Fractal Statistics', 'Generated {}'.format(datenow)])

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
            headers.insert(0, 'Scale')
            write_results.writerow(headers)

            # Writing Data Columns
            for row in rows:
                write_results.writerow(row)

            # Rescale Range
            write_results.writerow('')
            write_results.writerow(['Rescale Range:'])
            write_results.writerow(['Scale', 'RescaleRange'])
            for scale, rr in fractalResults['rescaleRange'].items():
                write_results.writerow(['fullSeries / {} : {} day chunks'.format(scale, refScales[scale]), rr])


