import csv
import os
from datetime import datetime

def writeCSV(stats):
    now = datetime.now()
    datenow = now.strftime("%m-%d-%Y %H:%M:%S")
    output_file = "fractalmarketslab/exports/portfolio/signals.csv"
    with open(output_file, mode='w') as resultsfile:
        write_results = csv.writer(resultsfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)    
        write_results.writerow([
            'Ticker', 
            'Current Price',
            'DonchianLow',
            'DonchianHigh',
            'UpperVol',
            'LowerVol',
            'ImpliedVol',
            'VolumeChange',
            'UpperRange',
            'LowerRange',
            'PercentDownside',
            'PercentUpside',
            'Signal'
            ])
        for ticker, data in stats.items():
            write_results.writerow([
                ticker,
                data['currentPrice'],
                data['donchian']['low'],
                data['donchian']['high'],
                data['vol']['upper'],
                data['vol']['lower'],
                data['vol']['implied'],
                data['vol']['volumeChange'],
                data['range']['upper'],
                data['range']['lower'],
                data['range']['downside'],
                data['range']['upside'],
                data['signal']
            ])