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


def save_output(cleardb=False, output='json'):
    FILES = "lab/correlations/output/files"
    JSON = "lab/correlations/output/json/correlations.json"
    Stock = apps.get_model('database', 'Stock')
    Correlations = apps.get_model('database', 'Correlation')
    if (cleardb):
        Correlations.objects.all().delete()
        print('DB Cleared')
    if (output == 'files'):
        files = os.listdir(FILES)

        for txtf in files:
            ticker = txtf.split('.').pop(0)
            if (ticker):
                try:
                    stock = Stock.objects.get(ticker=ticker)
                except:
                    continue

                print(ticker)
                with open(os.path.join(FILES, txtf), 'r') as f:
                    correlations = json.loads(f.read())
                try:
                    for corrs in correlations:
                        Correlations.objects.create(
                            stock=stock,
                            comparand=corrs['comparand'],
                            rvalue=corrs['rvalue']
                        )
                    os.rename(os.path.join(FILES, txtf), os.path.join(FILES, 'processed/', txtf))
                except:
                    print('Could not save {}'.format(ticker))

    if (output == 'json'):
        with open(JSON, 'r') as jsonfile:
            correlations = json.loads(jsonfile.read())
            for ticker, data in correlations.items():
                stock = Stock.objects.get(ticker=ticker)
                print("Saving: {}".format(ticker))
                for item in data:
                    try:
                        Correlations.objects.create(
                            stock=stock,
                            comparand=item['comparand'],
                            rvalue=item['rvalue']
                        )
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
