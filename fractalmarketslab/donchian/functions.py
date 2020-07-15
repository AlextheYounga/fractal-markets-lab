import statistics
import json

# Returns a list of items from a nested object.
def extractData(data, key):
    values = []
    if (type(key) == list):
        if len(key) == 2:
            for i, row in data.items():
                value = row[key[0]][key[1]]
                values.append(value)
        if len(key) == 3:
            for i, row in data.items():
                value = row[key[0]][key[1]][key[2]]
                values.append(value)
        if len(key) == 4:
            for i, row in data.items():
                value = row[key[0]][key[1]][key[2]][key[3]]
                values.append(value)
        if len(key) == 5:
            for i, row in data.items():
                value = row[key[0]][key[1]][key[2]][key[3]][key[4]]
                values.append(value)
        if len(key) > 5:
            return 'Nest level too deep to retrieve via function.'
    else:
        for i, row in data.items():
            value = row[key]
            values.append(value)
    return values

def consecutiveDays(prices):
    upDays = 0
    downDays = 0
    for i, price in enumerate(prices):
        percentChange = (price - prices[i + 1]) / prices[i + 1]
        if percentChange > 0:
            upDays = upDays + 1
        else: 
            break
    for i, price in enumerate(prices):
        percentChange = (price - prices[i + 1]) / prices[i + 1]
        if percentChange < 0:
            downDays = downDays + 1
        else: 
            break
    return upDays, downDays


def trendAnalysis(prices):
    analysis = {}
    consecutiveUps, consecutiveDowns = consecutiveDays(prices)
    downDays = []
    upDays = []
    for i, price in enumerate(prices):
        if (i + 1 in range(-len(prices), len(prices))):
            percentChange = (price - prices[i + 1]) / prices[i + 1] 
            if percentChange > 0:
                upDays.append(percentChange)
            if percentChange <= 0:
                downDays.append(percentChange)
        else:
            continue

    analysis['upDays'] = { 
        'count': len(upDays),
        'consecutive': consecutiveUps,
        'average': "{}%".format(statistics.mean(upDays) * 100)
    }
    
    analysis['downDays'] = { 
        'count': len(downDays),
        'consecutive': consecutiveDowns,
        'average': "{}%".format(statistics.mean(downDays) * 100)
    }

    return analysis

    
        
