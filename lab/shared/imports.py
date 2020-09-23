from datetime import datetime, timedelta
import requests
import json
import csv

def parseCSV(file):
    with open('lab/imports/{}'.format(file), newline='', encoding='utf-8') as csvfile:
        asset_data = {}
        reader = csv.DictReader(csvfile)

        for i, row in enumerate(reader):
            # Using powers of 2
            rows = {
                'date': row['\ufeffDate'] if row['\ufeffDate'] else '',
                'close': row['Close'] if row['Close'] else 0
            }
            # Append value dictionary to data
            asset_data[i] = rows
    return asset_data