import json
from ..shared.functions import *
from ..shared.imports import *
import math
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.stats import norm
import numpy as np
import pandas as pd
from tabulate import tabulate

# Variance/Covariance VAR analysis
def varCovar(ticker):
    asset_data = getShortTermPrices(ticker)

    prices = extractData(asset_data, 'close')
    series = pd.Series(prices)
    returns = series.pct_change()
    mean = np.mean(returns)
    stdev = np.std(returns)

    var90 = norm.ppf(1 - 0.9, mean, stdev)
    var95 = norm.ppf(1 - 0.95, mean, stdev)
    var99 = norm.ppf(1 - 0.99, mean, stdev)

    print(tabulate([['90%', var90], ['95%', var95], ['99%', var99]], headers=['Confidence Level', 'Value at Risk']))

    # Graph results
    returns.hist(bins=40, density=True, histtype='stepfilled', alpha=0.5)
    x = np.linspace(mean - 3*stdev, mean + 3*stdev, 100)
    plt.plot(x, norm.pdf(x, mean, stdev), "r")
    plt.show()

    return




