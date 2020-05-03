# from .rescale_range import *
from .rescale_test import *
from .functions import *
import json



# print(json.dumps(returns, indent=1))
# print(json.dumps(rangeData, indent=1))
# tradeChunks = chunkedAverages(returns, 16)
# print(json.dumps(tradeChunks, indent=1))
print(json.dumps(rangeStats, indent=1))

# print(json.dumps(list(chunks(returns, 30)), indent=1))
# print(list(chunks(returns, 30)))


