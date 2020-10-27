from .api import syncStocks
import json
import csv
import os

stocks = syncStocks()
print(json.dumps(len(stocks), indent=1))