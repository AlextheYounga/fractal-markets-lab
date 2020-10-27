import django
from django.apps import apps
import json
import os
import sys
from ..functions import *
from ...core.functions import *
from ...core.api import quoteStatsBatchRequest
django.setup()

tickers = ['SAM', 'WDFC', 'VOXX']

for ticker in tickers:


    keyStats = {
        'ticker': ticker,
        'name': stock.name,
        'lastPrice': price,
        'week52': stats['week52high'],
        'ttmEPS': ttmEPS,
        'reportedEPS': earningsChecked['actual'],
        'reportedConsensus': earningsChecked['consensus'],
        'peRatio': stats['peRatio'],
        'day5ChangePercent': stats['day5ChangePercent'],
        'month1ChangePercent': stats['month1ChangePercent'],
        'ytdChangePercent': stats['ytdChangePercent'],
        'day50MovingAvg': stats['day50MovingAvg'],
        'day200MovingAvg': stats['day200MovingAvg'],
        'fromHigh': fromHigh,
    }