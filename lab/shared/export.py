import csv
import os
import sys


# Data must be dictionary
def writeCSV(data, output):
    output_file = "lab/exports/{}".format(output)
    with open(output_file, mode='w') as resultsfile:
        write_results = csv.writer(resultsfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        write_results.writerow([
            data[0].keys()
        ])
        for row in data.items():
            write_results.writerow([
                row.values()
            ])
