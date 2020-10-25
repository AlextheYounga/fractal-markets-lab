import django
from django.apps import apps
django.setup()


def uniqueField(model, table, field):
    Model = apps.get_model('database', model)
    rows = Model.objects.raw('SELECT * FROM {} WHERE id IN (SELECT MIN(id) FROM database_stock GROUP BY {}) ORDER BY {}'.format(table, field, field))

    return rows


# chase.py
# Data must conform to this structure:
# data = {
#     'Model': {
#         'key': data
#     },
# }
def saveDynamic(data, stock):
    if (isinstance(data, dict)):
        for model, values in data.items():
            Model = apps.get_model('database', model)
            model_query = Model.objects.filter(stock=stock)
            if (model_query.count() == 0):
                Model.objects.create(**values)
            else:
                del values['stock']
                model_query.update(**values)

        return True
    else:
        return 'Data must be in dict form'
