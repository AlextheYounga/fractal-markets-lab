import django
from iexfinance.stocks import Stock
from ...core.api import syncStocks, companyBatchRequest
from ...core.functions import chunks
from django.apps import apps
import json
import sys
import os
django.setup()


Stock = apps.get_model('database', 'Stock')

stocks = syncStocks()
tickers = [stock['symbol'] for stock in stocks]
chunked_tickers = chunks(tickers, 100)

for i, chunk in enumerate(chunked_tickers):
    batch = companyBatchRequest(chunk)

    for i, info in batch.items():
        quote = info['quote'] if ('quote' in info) and info['quote'] else False
        company = info['company'] if ('quote' in info) and info['company'] else False

        if (company and quote):
            if (quote.get('companyName', False) or company.get('companyName', False)):
                Stock.objects.update_or_create(
                    ticker=quote['symbol'],
                    defaults={
                        'name': quote.get('companyName') if ('companyName' in quote) else company.get('companyName'),
                        'lastPrice': quote.get('lastPrice', None),
                        'index': quote.get('primaryExchange', None),
                        'sector': company.get('sector', None),
                        'industry': company.get('industry', None),
                        'employees': company.get('employees', None),
                        'description': company.get('description', None),
                    }
                )
                print('saved {}'.format(quote['symbol']))
