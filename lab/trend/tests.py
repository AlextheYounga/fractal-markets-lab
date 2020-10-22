import django
from django.apps import apps
django.setup()

Stock = apps.get_model('database', 'Stock')

stocks = Stock.objects.order_by('ticker').distinct()

# print(len(stocks))
for stock in stocks:
    print(stock)