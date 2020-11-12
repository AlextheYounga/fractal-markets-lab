from iexfinance.stocks import get_market_gainers
from dotenv import load_dotenv
from django.apps import apps
from ..core.output import printTable
from .functions import *
import requests
import json
import os
import texttable
os.environ['DJANGO_SETTINGS_MODULE'] = 'lab.settings'
load_dotenv()

Stock = apps.get_model('database', 'Stock')
Earnings = apps.get_model('database', 'Earnings')
Watchlist = apps.get_model('database', 'Watchlist')
gainers = get_market_gainers()

for i, mover in enumerate(gainers):
    print(i + 1)
    ticker = mover.get('symbol', None)
    price = mover.get('latestPrice', None)
    index = mover.get('primaryExchange', None)
    companyName = mover.get('companyName', None)
    peRatio = mover.get('peRatio', None)
    week52high = mover.get('week52High', None)
    marketCap = mover.get('marketCap', None) / 1000000 if (mover.get('marketCap')) else None
    changePercent = mover.get('changePercent', None) * 100 if (mover.get('changePercent')) else None
    ytdChange = mover.get('ytdChange', None) * 100 if (mover.get('ytdChange')) else None
    fromHigh = round((price / week52high) * 100, 3) if (price and week52high) else None

    if (price and isinstance(price, float)):
        stock, created = Stock.objects.update_or_create(
            ticker=ticker,
            defaults={
                'name': companyName,
                'lastPrice': price,
                'index': index
            },
        )
    else:
        continue

    if (fromHigh and ((fromHigh < 105) and (fromHigh > 95))):
        earningsData = getEarnings(ticker)
        if (earningsData and isinstance(earningsData, dict)):
            print('{} ---- Checking Earnings ----'.format(ticker))
            earningsChecked = checkEarnings(earningsData)

            data_for_db = {
                'Valuation':  {
                    'peRatio': peRatio,
                },
                'Trend': {
                    'week52': week52high,
                    'fromHigh': fromHigh
                },
                'Earnings': {
                    'reportedEPS': earningsChecked['actual'],
                    'reportedConsensus': earningsChecked['consensus'],
                },
            }

            dynamicUpdateCreate(data_for_db, stock)

            if (earningsChecked['improvement'] == True):
                keyStats = {
                    'week52': week52high,
                    'reportedEPS': earningsChecked['actual'],
                    'reportedConsensus': earningsChecked['consensus'],
                    'peRatio': peRatio,
                    'fromHigh': fromHigh,

                }
                Watchlist.objects.update_or_create(
                    stock=stock,
                    defaults=keyStats
                )
                print('{} saved to Watchlist'.format(ticker))

    stockdata = {
        'ticker': ticker,
        'companyName': companyName,
        'latestPrice': price,
        'changePercent': changePercent,
        'ytdChange': ytdChange,
        'week52High': week52high,
        'fromHigh': fromHigh,
        'volume': "{}k".format(mover.get('volume', None) / 1000) if (mover.get('volume')) else None,
        'previousVolume': "{}k".format(mover.get('previousVolume', None) / 1000) if (mover.get('previousVolume')) else None,
        'peRatio': peRatio,
        'marketCap': marketCap,
        'primaryExchange': index,
    }
    print('here')
    printTable(stockdata)
