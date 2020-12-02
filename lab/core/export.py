import csv
import sys
import os


# Data must be list of dicts
def writeCSV(data, output, append=False):
    output_file = "lab/exports/{}".format(output)
    if (not os.path.exists(output_file) or (append == False)):
        with open(output_file, mode='w') as resultsfile:
            write_results = csv.writer(resultsfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            write_results.writerow(
                data[0].keys()
            )
            for row in data:
                write_results.writerow(
                    row.values()
                )
        return
    else:
        with open(output_file, mode='a') as resultsfile:
            write_results = csv.writer(resultsfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in data:
                write_results.writerow(
                    row.values()
                )
        return
