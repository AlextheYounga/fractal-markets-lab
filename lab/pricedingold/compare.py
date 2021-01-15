import os
import sys
from..core.api import getHistoricalData
from ..core.functions import extract_data
from .gold import read_historical_gold_prices
from matplotlib import pylab
import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv
load_dotenv()

def price_in_gold(ticker, timespan='5y'):
    asset_prices = getHistoricalData(ticker, timespan)
    gold_prices = read_historical_gold_prices()


