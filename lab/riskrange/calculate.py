import statistics
import math
import json
import sys
from .methodology import rangeRules
from ..core.output import printTable
from ..fintwit.tweet import send_tweet
from .vix.equation import modified_vix


# def calculateRange(ticker):
    # data = rangeRules(ticker)
    # printTable(data[ticker])
print(modified_vix('TSLA'))

