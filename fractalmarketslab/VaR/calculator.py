import statistics
from scipy import stats
import json
from .functions import *
from ..imports.api import *
import math
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def calculate(ticker):
    asset_data = getShortTermPrices(ticker)

    prices = extractData(asset_data, 'close')
    returns = prices.pct_change()


