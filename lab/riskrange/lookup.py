import statistics
import math
import json
from .methodology import *
from .output import printTable
from ..shared.functions import *
from ..shared.api import *
import texttable


def rangeLookup(ticker):
    data = rangeRules(ticker)
    printTable(ticker, data)
    
