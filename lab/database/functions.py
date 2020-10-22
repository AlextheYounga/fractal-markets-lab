import django
from django.apps import apps
django.setup()

Stock = apps.get_model('database', 'Stock')

def uniqueStocks():
    Stock.objects.filter(stuff).values("ticker").annotate(n=models.Count("pk"))
    for stock in Stock.objects.all():
        print(stock.ticker)

