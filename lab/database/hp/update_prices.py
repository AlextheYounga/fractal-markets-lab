import django
from django.apps import apps
from dotenv import load_dotenv
from datetime import datetime, date, timedelta
from ...core.api import getHistoricalData, batchHistoricalData
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
        return '2y'
    if (diff < 1825):
        return '5y'


def batch_refresh_prices(batch, timeframe):
    print('Running...')
    HistoricalPrices = apps.get_model('database', 'HistoricalPrices')
    Stock = apps.get_model('database', 'Stock')
    data = batchHistoricalData(batch, timeframe, priceOnly=True)

    for ticker, stats in data.items():
        print('Saving {}'.format(ticker))

        stock, created = Stock.objects.update_or_create(
            ticker=ticker
        )

        defaults = {
            'prices': stats['chart'],
            'datapoints': len(stats['chart'])
        }

        hp = HistoricalPrices.objects.update_or_create(
            stock=stock,
            defaults=defaults
        )


def update_prices(stock):
    HistoricalPrices = apps.get_model('database', 'HistoricalPrices')

    if (HistoricalPrices.objects.filter(stock=stock).count() != 0):
        hp = HistoricalPrices.objects.get(stock=stock)
        prices = hp.prices
        lastdate = datetime.strptime(prices[-1]['date'], '%Y-%m-%d')
        today = datetime.now()

        diff = abs((today - lastdate).days)

        if (diff <= 3):
            return

        latest_prices = getHistoricalData(stock.ticker, calculate_range(diff), priceOnly=True)

        for i, day in enumerate(list(reversed(latest_prices))):
            prices.append(day)
            if (day['date'] == prices[-1]['date']):
                break

        hp.prices = prices
        hp.datapoints = len(hp.prices)
        hp.save()

    else:
        prices = getHistoricalData(stock.ticker, 'max', priceOnly=True)
        hp = HistoricalPrices.objects.create(
            stock=stock,
            prices=prices,
            datapoints=len(prices)
        )


def refresh_one(ticker, timeframe='max'):
    """
    There appears to be a bug in IEX console where some tickers are not available on batch requests.
    I made this as a workaround.

    Command:
    python -c 'from lab.database.hp.update_prices import refresh_one; print(refresh_one("XOP"))'
    """
    HistoricalPrices = apps.get_model('database', 'HistoricalPrices')
    Stock = apps.get_model('database', 'Stock')

    prices = getHistoricalData(ticker, timeframe, priceOnly=True)

    stock = Stock.objects.get(ticker=ticker)

    defaults = {
        'prices': prices,
        'datapoints': len(prices)
    }

    hp, created = HistoricalPrices.objects.update_or_create(
        stock=stock,
        defaults=defaults
    )

    print('Saved {}, Created: {}'.format(ticker, created))
