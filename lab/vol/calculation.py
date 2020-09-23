from ..shared.functions import *
from ..shared.api import *

assetData = getShortTermData(ticker)
prices = removeZeroes(extractData(assetData, 'close'))
vol = calculateVol(list(reversed(prices)))
print vol