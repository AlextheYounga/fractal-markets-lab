import statistics
import math
import json
from .methodology import *
from .output import printTable
from ..core.functions import *
from ..core.api import *
import texttable


def rangeLookup(ticker):
    data = rangeRules(ticker)
    printTable(ticker, data)
    
