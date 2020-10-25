import statistics
import math
import json
from .export import *
from .output import printTable
from .methodology import *
from ..core.functions import *
from ..core.api import *
import texttable


portfolio = [
    'GDXJ',
    'GDX',
    # 'UEC',
    # 'DBA',
    # 'SLV',
]

signalArray = {}
for ticker in portfolio:
    data = rangeRules(ticker)
    signalArray[ticker] = data[ticker]

    printTable(ticker, data)

writeCSV(signalArray)
