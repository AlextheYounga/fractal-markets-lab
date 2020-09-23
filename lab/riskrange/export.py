import csv
import os
from datetime import datetime
from datetime import date
import sys


def writeCSV(stats):
    from datetime import date


# now = date.today()
    today = date.today().strftime('%m-%d')
    output_file = "lab/exports/portfolio/signals{}.csv".format(today)
    with open(output_file, mode='w') as resultsfile:
        write_results = csv.writer(resultsfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        write_results.writerow([
            'Ticker',
            'Current Price',
            'LowerRange',
            'UpperRange',
            'Lower StDev',
            'Upper StDev',
            'TechnicalLow',
            'TechnicalHigh',
            'ShortTermDonchianLow',
            'ShortTermDonchianHigh',
            'ImpliedVol',
            'VolumeChange',
            'PercentDownside',
            'PercentUpside',
            'Signal',
        ])
        for ticker, data in stats.items():
            write_results.writerow([
                ticker,
                data['currentPrice'],
                data['range']['lower'],
                data['range']['upper'],
                data['vol']['lower'],
                data['vol']['upper'],
                data['donchian']['technicalLow'],
                data['donchian']['technicalHigh'],
                data['donchian']['shortTermLow'],
                data['donchian']['shortTermHigh'],
                data['vol']['implied'],
                data['vol']['volumeChange'],
                data['range']['downside'],
                data['range']['upside'],
                data['signal'],
            ])
