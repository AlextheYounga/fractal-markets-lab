import django
from django.apps import apps
from dotenv import load_dotenv
from datetime import datetime, date, timedelta
from ...core.api import getHistoricalData
from django.core.exceptions import ObjectDoesNotExist
import json
import sys
django.setup()


def calculate_range(diff):
    if (diff < 5):
        return '5d'
    if (diff < 30):
        return '1m'
    if (diff < 90):
        return '3m'
    if (diff < 180):
        return '6m'
    if (diff < 365):
        return '1y'
    if (diff < 730):
        return '1y'
    if (diff < 1825):
        return '1y'


def update_record_prices(stock):
    HistoricalPrices = apps.get_model('database', 'HistoricalPrices')

    try:
        hp = HistoricalPrices.objects.get(stock=stock)    
        prices = hp.prices
        lastdate = datetime.strptime(prices[-1]['date'], '%Y-%m-%d')
        today = datetime.now()

        print(prices[-1]['date'])

        if (today.date() == lastdate.date()):
            return

        diff = abs((today - lastdate).days)
        latest_prices = getHistoricalData(stock.ticker, calculate_range(diff), priceOnly=True, sandbox=True)
        
        
        for i, day in enumerate(list(reversed(latest_prices))):
            prices.append(day)
            if (day['date'] == prices[-1]['date']):
                break      

        hp.prices = prices
        hp.datapoints = len(hp.prices)
        hp.save()

        return hp
        
    except ObjectDoesNotExist:
        prices = getHistoricalData(stock.ticker, '5y', priceOnly=True, sandbox=True)
        hp = HistoricalPrices.objects.create(
            stock=stock,
            prices=prices,
            datapoints=len(prices)
        )

        return hp




