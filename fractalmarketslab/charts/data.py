import csv
import statistics 
from .functions import extract_data


with open('fractalmarketslab/imports/SPX_volatility.csv', newline='', encoding='utf-8') as csvfile:
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
averages = {
    'trade': statistics.mean(prices[:16]),
    'trend': statistics.mean(prices[:64]),
    'tail': statistics.mean(prices[:757]),
}