import statistics
import json
import sys
import os



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


def longestStretch(data):
    upStreaks = {}
    downStreaks = {}
    strkTemp = {}
    streak = 0
    index = 0
    for i, day in data.items():
        if (i - 1 > 0):
            percentChange = (day['close'] - data[i - 1]['close']) / data[i - 1]['close']
            if percentChange > 0:
                streak = streak + 1
                strkTemp[streak] = day
            else:
                index = index + 1
                upStreaks[index] = strkTemp
                streak = 0
                strkTemp = {}

    maxcount = max(len(v) for v in upStreaks.values())
    longest = [k for k, v in upStreaks.items() if len(v) == maxcount][0]
    upStreaks = upStreaks[longest]
    strkTemp = {}
    streak = 0
    index = 0
    for i, day in data.items():
        if (i - 1 > 0):
            percentChange = (day['close'] - data[i - 1]['close']) / data[i - 1]['close']
            if percentChange < 0:
                streak = streak + 1
                strkTemp[streak] = day
            else:
                index = index + 1
                downStreaks[index] = strkTemp
                streak = 0
                strkTemp = {}

    maxcount = max(len(v) for v in downStreaks.values())
    longest = [k for k, v in downStreaks.items() if len(v) == maxcount][0]
    downStreaks = downStreaks[longest]

    return upStreaks, downStreaks


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



