import json
import redis
import sys
import os


def allowed_key(key):
    """
    A way of standardizing keys and preventing bad inserts.

    Parameters
    ----------
    key      :string
             key to be compared with array.

    Returns
    -------
    bool
    """
    allowed = [
        # Stocks
        'name',
        'industry',
        'employees',
        'price',
        'sector',
        'description',
        # Earnings
        'ttmEPS',
        # Financials
        'reportDate',
        'netIncome',
        'netWorth',
        'shortTermDebt',
        'longTermDebt',
        'totalCash',
        'totalDebt',
        'debtToEquity',
        'priceToSales',
        'EBITDA',
        'freeCashFlow',
        'freeCashFlowPerShare',
        'freeCashFlowYield',
        'longTermDebtToEquity',
        # Trend
        'week52',
        'day5ChangePercent',
        'month1ChangePercent',
        'ytdChangePercent',
        'day50MovingAvg',
        'day200MovingAvg',
        'avgPricetarget',
        'highPriceTarget',
        'fromPriceTarget',
        'fromHigh',
        # Valuation
        'peRatio',
        # HistoricalPrices
        'prices',
        'prices-datapoints',
        # Correlations
        'rvalue',
        'datapoints'
    ]
    if (key in allowed):
        return True
    else:
        return False


def rdb_save_stock(ticker, data):
    """
    Dynamically saves data to the redis db under the typecast 'stock-'.
    Refer to redisdb/schema.py to see standard schema.
    Make sure not to include ticker in the data object. Ticker should be pass separately.

    Parameters
    ----------
    ticker    :string
    data      :dict
               dict object of financial data

    Returns
    -------
    bool
    """

    r = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)
    keys = data.keys()

    for key in keys:
        if (key == ticker):
            # Prevent bad data insert
            continue
        if (allowed_key(key)):            
            r.set('stock-{}-{}'.format(ticker, key), data[key])            
        else:
            print(key+' is not an allowed insert key. Please add to list of allowed keys if you wish to insert.')            
