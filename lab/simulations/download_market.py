import django
from django.apps import apps
from ..core.api import batchHistoricalData
from ..database.functions import saveHistoricalPrices
from ..core.functions import chunks
from ..macro.functions import getETFs
from django.apps import apps
import json
import sys
import os
django.setup()

tickers = getETFs(tickersonly=True)

print('Running...')
chunked_tickers = chunks(tickers, 100)
for i, chunk in enumerate(chunked_tickers):
    batch = batchHistoricalData(chunk, '5y', priceOnly=True)

    for ticker, stockinfo in batch.items():
        print('Chunk {}: {}'.format(i, ticker))
        if (stockinfo.get('chart', False)):
            historicalprices = stockinfo.get('chart')
            saveHistoricalPrices(ticker, historicalprices)
