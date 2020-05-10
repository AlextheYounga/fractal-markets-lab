# from .rescale_range import *
from .rescale_example import *
from .functions import *
import json
from timeit import default_timer as timer

start = timer()

print(die)
# for i, section in fractalResults['regressionResults'].items():
#     print(section['fractalDimension'])
# print(json.dumps(fractalResults, indent=1))
# print(json.dumps(rangeStats, indent=1))


if (done == True):
    end = timer()
    print("\n" + "Done")
    print("Time elapsed:", end - start, "seconds")


# print(json.dumps(rescaleRanges, indent=1))
# print(json.dumps(fractalResults, indent=1))
# print(json.dumps((logRR, logScales), indent=1))
# print(json.dumps(logRR, indent=1))
# print(json.dumps(rangeStats, indent=1))
# print(json.dumps(rangeStats['4']['analysis']['rescaleRangeAvg'], indent=1))
# print(json.dumps(rangeData, indent=1))
# print(type(rangeData[15819]['stats']['32']['runningTotal']))
