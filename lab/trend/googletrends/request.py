from pytrends.request import TrendReq
from datetime import datetime
from ..functions import getPennyStocks
import colored
from colored import stylize
import time
import redis
import json
import sys


def stock_search_trends():
    """
    This function will request search query data from Google for all stocks listed on IEX. 
    It is purposely slow. I have added a 30 second wait limit between each request due to the size of the requests we're 
    going to make and the unpredictability of Google's rate limits. To ensure we keep Google happy, 
    """
    tickers = getPennyStocks()
    for i, ticker in enumerate(tickers):
        if (i > 4):
            query = ticker+' stock'
            pytrends = TrendReq(hl='en-US', tz=360)
            pytrends.build_payload([query], cat=0, timeframe='today 12-m', geo='', gprop='')
            interest = pytrends.interest_over_time().to_dict()
            r = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)
            data = {}
            if (interest):
                for date, value in interest[query].items():        
                    data[date.strftime('%Y-%m-%d')] = value
                
                r.set('trends-'+ticker+'-interest', json.dumps(data))
                print(stylize("Request {} Saved {}".format(i, ticker), colored.fg("green")))
            time.sleep(5)
        
