from .data import *
from .functions import *
import json

# for i, value in enumerate(prices):
#     change = {
#         'dayChange': (prices[i] - prices[i + 1]) / prices[i + 1] if  prices[i + 1] else 0,
#         'trade': (prices[i] - prices[i + 16]) / prices[i + 16] if  prices[i + 16] else 0,
#         'trend': (prices[i] - prices[i + 64]) / prices[i + 64] if  prices[i + 64] else 0,
#         'tail': (prices[i] - prices[i + 757]) / prices[i + 757] if  prices[i + 757] else 0,
#     }

# for i, value in enumerate(prices):
#     changeData = percentChange(prices, i)
#     # print(changeData)
#     print(changeData['dayChange'])
#     break 

print(json.dumps(volData, indent=1))

