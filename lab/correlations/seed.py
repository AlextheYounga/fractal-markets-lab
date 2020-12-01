import time
import django
from django.apps import apps
from ..core.functions import extract_data, chunks
from datetime import datetime, timedelta
import json
import sys
import os
from dotenv import load_dotenv
load_dotenv()
django.setup()


def save_output():
    OUTPUT = "lab/correlations/output/"
    Stock = apps.get_model('database', 'Stock')
    Correlations = apps.get_model('database', 'Correlation')
    Correlations.objects.all().delete()
    print('DB Cleared')
    files = os.listdir(OUTPUT)

    for txtf in files:
        ticker = txtf.split('.').pop(0)        
        if (ticker):
            try:
                stock = Stock.objects.get(ticker=ticker)
            except:
                continue
            
            print(ticker)            
            with open(os.path.join(OUTPUT, txtf), 'r') as f:
                correlations = json.loads(f.read())
            try:
                for corrs in correlations:
                    Correlations.objects.create(
                        stock=stock,
                        comparand=corrs['comparand'],
                        rvalue=corrs['rvalue']
                    )
                os.rename(os.path.join(OUTPUT, txtf), os.path.join(OUTPUT, 'processed/', txtf))
            except:
                print('Could not save {}'.format(ticker))


# FILES = "lab/correlations/results/files"
# json_output = {}
# files = os.listdir(FILES)
# i = 0 
# for f in files:
#     i += 1
#     ticker = f.split('.').pop(0)
#     print(i, ticker)
#     if (ticker):        
#         json_output[ticker] = []
#         with open(os.path.join(FILES, f), 'r') as txtfile:
#             if (i == 947):
#                 print(f)
#             correlations = json.loads(txtfile.read())
#         for corrs in correlations:
#             data = {'comparand': corrs['comparand'], 'rvalue': corrs['rvalue']}
#             json_output[ticker].append(data)
    
# with open(os.path.join("lab/correlations/results/", "correlations.json")) as json_file:
#     json.dump(correlations, json_file)