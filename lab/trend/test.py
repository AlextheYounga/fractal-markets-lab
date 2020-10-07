import statistics
import json
import os
import sys
import texttable
from .functions import *
from ..shared.functions import *
from ..shared.api import getCurrentPrice
from ..shared.imports import parseCSV
from dotenv import load_dotenv
import requests
load_dotenv()

nasdaq = parseCSV('NasdaqComposite.csv')

print(nasdaq[0].keys())
headers = nasdaq[0].keys()
table = texttable.Texttable()
table.header(headers)
for i, stock in nasdaq.items():
    table.add_rows([stock.values()], header=False)

print(table.draw())
