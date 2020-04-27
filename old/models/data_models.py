from django.db import models
from jsonfield import JSONField
from datetime import date
from termcolor import colored, cprint
import csv

# Create your models here.

def volatilityData():
    with open('fractal_markets_lab/probability/data/SPX_volatility.csv', newline='', encoding='utf-8') as csvfile:
        data = {}
        reader = csv.DictReader(csvfile)        
        for i, row in reader:
            # print(row.keys())
            values = {
                'assetName': 'S&P 500',
                'date': row['\ufeffDate'] if row['\ufeffDate'] else '',
                'open': row['Open'] if row['Open'] else 0,
                'close': row['Close'] if row['Close'] else 0,
                'logReturns':row['Log Returns'] if row['Log Returns'] else 0,
                'low': row['Low'] if row['Low'] else 0,
                'high': row['High'] if row['High'] else 0,
                'lowRR': row['LowRR'] if row['LowRR'] else 0,
                'highRR': row['HighRR'] if row['HighRR'] else 0,
                'volIndex': row['VIX'] if row['VIX'] else 0,
                'volume': row['Volume'] if row['Volume'] else 0,
                'putCallRatio':row['PutCall'] if row['PutCall'] else 0,
                'stats': {
                    'trade': {
                        'stdev':row['Trade StDev'] if row['Trade StDev'] else 0,
                        'impliedVol':row['Trade IV'] if row['Trade IV'] else 0,
                    },
                    'trend': {
                        'stdev':row['Trend StDev'] if row['Trend StDev'] else 0,
                        'impliedVol':row['Trend IV'] if row['Trend IV'] else 0,
                    },
                    'tail': {
                        'stdev':row['Tail StDev'] if row['Tail StDev'] else 0,
                        'impliedVol':row['Tail IV'] if row['Tail IV'] else 0,
                    }
                }
            }
            data[i] = values
        return
    return data