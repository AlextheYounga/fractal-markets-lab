import os
import sys
import requests
from ..core.functions import extract_data
from ..core.imports import parseCSV
from dotenv import load_dotenv
load_dotenv()


def read_historical_gold_prices():
    data = parseCSV('lab/pricedingold/data/goldprices1970.csv', fullPath=True)  
    gold_prices = []
    for row in data:
        d = {'Date': row['Date'], 'Close': row['Close']}
        gold_prices.append(d)

    return gold_prices



def fetch_gold_price():
    base_currency = 'USD'
    symbol = 'XAU'
    endpoint = '1999-12-24'
    access_key = os.environ.get("METALS_API_KEY")

    url = 'https://metals-api.com/api/'+endpoint+'?access_key='+access_key+'&base='+base_currency+'&symbols='+symbol
    print(url)
    sys.exit()

    try:
        gold_price = requests.get(url).json()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return None

    return gold_price
