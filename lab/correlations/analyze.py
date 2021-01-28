import django
from django.apps import apps
from ..core.functions import extract_data, chunks
from datetime import datetime
import json
import sys
import os
from dotenv import load_dotenv
from ..fintwit.tweet import send_tweet
load_dotenv()
django.setup()

Stock = apps.get_model('database', 'Stock')
Correlations = apps.get_model('database', 'Correlation')

correlations = Correlations.objects.filter(rvalue__gte=0.99)
inverse_correlations = Correlations.objects.filter(rvalue__lte=-0.90)
blacklist = ['Short', 'Inverse', 'Bear', 'Decline', 'Tail']

def is_short(n):
    for b in blacklist:
        if (b in n):
            return True
    return False

def print_correlation(corrs):
    for i in corrs[:100]:
        comparand = Stock.objects.get(ticker=i.comparand)
        if (is_short(i.stock.name)): continue
        if (is_short(comparand.name)): continue
        print("{}({}) - {}({}): {}".format(
            i.stock.name,
            i.stock.ticker,
            comparand.name,
            comparand.ticker,
            i.rvalue))

# print('Correlations')
# if (len(correlations) > 200):
#     print(len(correlations))
# else:
#     print_correlation(correlations)

print('Inverse')
# if (len(inverse_correlations) > 200):
#     print(len(inverse_correlations))
# else:
print_correlation(inverse_correlations)
