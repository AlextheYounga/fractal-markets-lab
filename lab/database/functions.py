import django
from django.apps import apps
django.setup()


def uniqueField(model, table, field):
    Model = apps.get_model('database', '{}'.format(model))
    rows = Model.objects.raw('SELECT * FROM {} WHERE id IN (SELECT MIN(id) FROM database_stock GROUP BY {}) ORDER BY {}'.format(table, field, field))

    return rows

def bulk_update_or_create(defaults=None, **kwargs):
    defaults = {'first_name': 'Bob'}
try:
    obj = Person.objects.get(first_name='John', last_name='Lennon')
    for key, value in defaults.items():
        setattr(obj, key, value)
    obj.save()
except Person.DoesNotExist:
    new_values = {'first_name': 'John', 'last_name': 'Lennon'}
    new_values.update(defaults)
    obj = Person(**new_values)
    obj.save()
