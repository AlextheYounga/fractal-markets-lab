import csv
import statistics 
from .functions import *


with open('fractalmarketslab/imports/VolSPX.csv', newline='', encoding='utf-8') as csvfile:
    volData = {}
    reader = csv.DictReader(csvfile)

    for i, row in enumerate(reader):

        values = {
            'assetName': 'S&P 500',
            'date': row['\ufeffDate'] if row['\ufeffDate'] else '',
            'open': row['Open'] if row['Open'] else 0,
            'close': row['Close'] if row['Close'] else 0,
            'logReturns': row['Log Returns'] if row['Log Returns'] else 0,
            'low': row['Low'] if row['Low'] else 0,
            'high': row['High'] if row['High'] else 0,
            'lowRR': row['LowRR'] if row['LowRR'] else 0,
            'highRR': row['HighRR'] if row['HighRR'] else 0,
            'volIndex': row['VIX'] if row['VIX'] else 0,
            'volume': row['Volume'] if row['Volume'] else 0,
            'putCallRatio': row['PutCall'] if row['PutCall'] else 0,
            
            'stats': {
                'dayChange': {},
                'trade': {
                    'stdev': row['Trade StDev'] if row['Trade StDev'] else 0,
                    'impliedVol': row['Trade IV'] if row['Trade IV'] else 0,
                },
                'trend': {
                    'stdev': row['Trend StDev'] if row['Trend StDev'] else 0,
                    'impliedVol': row['Trend IV'] if row['Trend IV'] else 0,
                },
                'tail': {
                    'stdev': row['Tail StDev'] if row['Tail StDev'] else 0,
                    'impliedVol': row['Tail IV'] if row['Tail IV'] else 0,
                }
            }
        }

        # Append value dictionary to data
        volData[i] = values

prices = extract_data(volData, 'close')
volume = extract_data(volData, 'volume')
vix = extract_data(volData, 'volIndex')
logReturns = extract_data(volData, 'logReturns')
putCall = extract_data(volData, 'putCallRatio')


averages = {
    'trade': {
         'prices': statistics.mean(prices[:16]),
         'volume': statistics.mean(volume[:16]),
         'vix': statistics.mean(vix[:16]),
    },
    'trend': {
         'prices': statistics.mean(prices[:64]),
         'volume': statistics.mean(volume[:64]),
         'vix': statistics.mean(vix[:64]),
    },
    'tail': {
        'prices': statistics.mean(prices[:757]),
        'volume': statistics.mean(volume[:757]),
        'vix': statistics.mean(vix[:757]),
    },
}

for i, value in enumerate(prices):
    changeData = percentChange(prices, i)
    volData[i]['stats']['dayChange']['price'] = changeData['dayChange']
    volData[i]['stats']['trade']['price'] = changeData['trade']
    volData[i]['stats']['trend']['price'] = changeData['trend']
    volData[i]['stats']['tail']['price'] = changeData['tail']

for i, value in enumerate(volume):
    changeData = percentChange(volume, i)
    volData[i]['stats']['dayChange']['volume'] = changeData['dayChange']
    volData[i]['stats']['trade']['volume'] = changeData['trade']
    volData[i]['stats']['trend']['volume'] = changeData['trend']
    volData[i]['stats']['tail']['volume'] = changeData['tail']

for i, value in enumerate(vix):
    changeData = percentChange(vix, i)
    volData[i]['stats']['dayChange']['vix'] = changeData['dayChange']
    volData[i]['stats']['trade']['vix'] = changeData['trade']
    volData[i]['stats']['trend']['vix'] = changeData['trend']
    volData[i]['stats']['tail']['vix'] = changeData['tail']


