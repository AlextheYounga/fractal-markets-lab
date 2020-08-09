# from .rescale_range import *
from .calculator import *
from .functions import *
import json
from timeit import default_timer as timer

start = timer()

# print(json.dumps(fractal_results, indent=1))



if (done == True):
    end = timer()
    print("\n" + "Done")
    print("Time elapsed:", end - start, "seconds")


# print(json.dumps(rescaleRanges, indent=1))
# print(json.dumps(fractal_results, indent=1))
# print(json.dumps((logRR, log_scales), indent=1))
# print(json.dumps(logRR, indent=1))
# print(json.dumps(range_stats, indent=1))
# print(json.dumps(range_stats['4']['analysis']['rescaleRangeAvg'], indent=1))
# print(json.dumps(rangeData, indent=1))
# print(type(rangeData[15819]['stats']['32']['runningTotal']))
