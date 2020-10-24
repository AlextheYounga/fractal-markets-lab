import django
from django.apps import apps
django.setup()


def uniqueField(model, table, field):
    Model = apps.get_model('database', model)
    rows = Model.objects.raw('SELECT * FROM {} WHERE id IN (SELECT MIN(id) FROM database_stock GROUP BY {}) ORDER BY {}'.format(table, field, field))

    return rows



