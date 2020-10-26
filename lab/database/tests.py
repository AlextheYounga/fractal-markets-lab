# from django.test import TestCase
# Create your tests here.
import os
import json
import sys
from ..core.functions import *
from ..core.imports import parseCSV

    
nasdaq = {'Nasdaq Composite': parseCSV('stocks/NasdaqComposite.csv') }
nasdaq['Nasdaq Composite'].update(parseCSV('stocks/NasdaqOthersListed.csv'))
dow = { 'Dow Jones Industrial Average': parseCSV('stocks/DowJones.csv') }
nyse = {'New York Stock Exchange': parseCSV('stocks/NYSE.csv') }
russell2k = { 'Russell 2000': parseCSV('stocks/Russell2000.csv') }
russell3k = { 'Russell 3000': parseCSV('stocks/Russell3000.csv') } 
spx = { 'S&P 500': parseCSV('stocks/S&P500.csv') }

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
