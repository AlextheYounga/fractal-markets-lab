import csv
import statistics
from scipy import stats
from .functions import *
import math
import sys

# Parsing csv data
with open('fractalmarketslab/imports/donchian.csv', newline='', encoding='utf-8') as csvfile:
    asset_data = {}
    reader = csv.DictReader(csvfile)

    for i, row in enumerate(reader):
        rows = {
            'date': row['\ufeffDate'] if row['\ufeffDate'] else '',
            'open': row['Open'] if row['Open'] else 0,
            'low': row['Low'] if row['Low'] else 0,
            'high': row['High'] if row['High'] else 0,
            'close': row['Close'] if row['Close'] else 0,                        
        }
        # Append value dictionary to data
        asset_data[i] = rows

prices = extractData(asset_data, 'close')

scales = {
    'trade': 16,
    'month': 22,
    'trend': 64,
    'tail': 756
}