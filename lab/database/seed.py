import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lab.settings")
# from .models import *
import json
import sys
from ..shared.functions import *
from ..shared.imports import parseCSV

    
nasdaq = {'Nasdaq Composite': parseCSV('NasdaqComposite.csv') }
nasdaq['Nasdaq Composite'].update(parseCSV('NasdaqOthersListed.csv'))
dow = { 'Dow Jones Industrial Average': parseCSV('DowJones.csv') }
nyse = {'New York Stock Exchange': parseCSV('NYSE.csv') }
russell2k = { 'Russell 2000': parseCSV('Russell2000.csv') }
russell3k = { 'Russell 3000': parseCSV('Russell3000.csv') } 
spx = { 'S&P 500': parseCSV('S&P500.csv') }

stocks = [
    nasdaq,    
    dow,
    nyse,
    russell2k,
    russell3k,
    spx
]

# print(json.dumps(stocks, indent=1))
# remove duplicates
for i, indices in enumerate(stocks):
    for index, stocks in indices.items():
        # print(len(stocks))
        for i, row in stocks.items():
            print(row['ticker'])
        # print(index)
        # Index(
        #     name=index,
        #     count=
        # )
