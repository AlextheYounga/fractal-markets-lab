import django
from django.apps import apps
from datetime import datetime
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


def dynamicUpdateCreate(data, find):
    """ 
    Parameters
    ----------
    data :  dict
            Data must conform to this structure:
                data = {
                    'Model': {
                    'column': value
                    },
                }
    find :  QuerySet object

    Returns
    -------
    boolean|string
    """
    if (isinstance(data, dict)):
        for model, values in data.items():
            Model = apps.get_model('database', model)
            Model.objects.update_or_create(
                stock=find,
                defaults=values,
            )
    else:
        return 'Data must be in dict structure'

    return True


def updatedToday(record):
    """ 
    Parameters
    ----------
    record :  Database record
              Checks to see if the record has already been updated today.
    Returns
    -------
    boolean
    """
    # TODO: Create function to check if record has already been updated, if so default to db records to save api requests.
