import django
from django.apps import apps
import sys
django.setup()


def uniqueField(model, table, field):
    Model = apps.get_model('database', model)
    rows = Model.objects.raw('SELECT * FROM {} WHERE id IN (SELECT MIN(id) FROM database_stock GROUP BY {}) ORDER BY {}'.format(table, field, field))

    return rows


def saveHistoricalPrices(ticker, api_data):
    Stock = apps.get_model('database', 'Stock')
    HistoricalPrices = apps.get_model('database', 'HistoricalPrices')
    stock, created = Stock.objects.update_or_create(
        ticker=ticker
    )
    if (isinstance(api_data, list)):
        histprices, created = HistoricalPrices.objects.update_or_create(stock=stock, defaults={'prices': api_data})
            

    
