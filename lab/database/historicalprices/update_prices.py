import django
from django.apps import apps
from dotenv import load_dotenv
from datetime import datetime, date, timedelta
from ...core.api import getHistoricalData
import json
import sys
django.setup()


def calculate_range(diff):
    if (diff < 5):
        return '5d'
    if (diff < 30):
        return '1m'
    if (diff < 90):
        return '3m'
    if (diff < 180):
        return '6m'
    if (diff < 365):
        return '1y'
    if (diff < 730):
        return '1y'
    if (diff < 1825):
        return '1y'


def update_record_prices(stock):
    HistoricalPrices = apps.get_model('database', 'HistoricalPrices')
    hp = HistoricalPrices.objects.get(stock=stock)

    if (hp):
        prices = hp.prices
        lastdate = datetime.strptime(prices[-1]['date'], '%Y-%m-%d')
        today = datetime.now()

        print(prices[-1]['date'])

        if (today.date() == lastdate.date()):
            return

        diff = abs((today - lastdate).days)
        api_range = datetime.strftime((lastdate + timedelta(days=1)), '%Y%m%d')
        latest_prices = getHistoricalData(stock.ticker, calculate_range(diff), priceOnly=True, sandbox=True)
        
        
        for i, day in enumerate(list(reversed(latest_prices))):      
            if (day['date'] == prices[-1]['date']):
                break
            del latest_prices[i]
        
    # TODO: Finish figuring out how to tack on remaining days to price list

        print(latest_prices)
        sys.exit()        

    else:
        print('else')
            
        
        

Stock = apps.get_model('database', 'Stock')
update_record_prices(Stock.objects.get(id=3517))


    
# python -c 'from lab.database.historicalprices.update_prices import update_record_prices; print(update_record_prices("EDV"))'



