from iexfinance.stocks import Stock, get_historical_data
from datetime import datetime
from dotenv import load_dotenv
import requests
import sys
import json
import os
load_dotenv()


def syncStocks():
    """
    Fetches all stocks from IEX 

    Returns
    -------
    object of all stocks 
    """
    try:
        url = 'https://cloud.iexapis.com/stable/ref-data/iex/symbols?token={}'.format(os.environ.get("IEX_TOKEN"))
        tickers = requests.get(url).json()
    except:
        #print("Unexpected error:", sys.exc_info()[0])
        return {}

    return tickers


def quoteStatsBatchRequest(batch, sandbox=False):
    """
    Fetches quotes and key stats for a batch of tickers. Max 100 tickers

    Parameters
    ----------
    batch       :list
                list of max 100 tickers
    sandbox     :bool
                Sets the IEX environment to sandbox mode to make limitless API calls for testing.

    Returns
    -------
    dict object of quotes and key stats for 100 tickers
    """
    domain = 'cloud.iexapis.com'
    key = os.environ.get("IEX_TOKEN")
    if (sandbox):
        domain = 'sandbox.iexapis.com'
        key = os.environ.get("IEX_SANDBOX_TOKEN")

    batch = ",".join(batch)  # Convert to comma-separated string
    try:
        url = 'https://{}/stable/stock/market/batch?symbols={}&types=quote,stats&token={}'.format(
            domain,
            batch,
            key
        )
        batch_request = requests.get(url).json()
    except:
        #print("Unexpected error:", sys.exc_info()[0])
        return {}

    return batch_request


def companyBatchRequest(batch, sandbox=False):
    """
    Fetches company info for a batch of tickers. Max 100 tickers

    Parameters
    ----------
    batch       :list
                list of max 100 tickers
    sandbox     :bool
                Sets the IEX environment to sandbox mode to make limitless API calls for testing.

    Returns
    -------
    dict object of company info for 100 tickers
    """
    domain = 'cloud.iexapis.com'
    key = os.environ.get("IEX_TOKEN")
    if (sandbox):
        domain = 'sandbox.iexapis.com'
        key = os.environ.get("IEX_SANDBOX_TOKEN")
    try:
        batch = ",".join(batch)  # Convert to comma-separated string
        url = 'https://{}/stable/stock/market/batch?symbols={}&types=quote,company&token={}'.format(
            domain,
            batch,
            key
        )
        batch_request = requests.get(url).json()
    except:
        #print("Unexpected error:", sys.exc_info()[0])
        return {}

    return batch_request


def getCurrentPrice(ticker, sandbox=False):
    """
    Fetches latest price

    Parameters
    ----------
    ticker      :string
    sandbox     :bool
                Sets the IEX environment to sandbox mode to make limitless API calls for testing.

    Returns
    -------
    latest price as float 
    """
    key = os.environ.get("IEX_TOKEN")
    if (sandbox):
        os.environ['IEX_API_VERSION'] = 'iexcloud-sandbox'
        key = os.environ.get("IEX_SANDBOX_TOKEN")
    try:
        stock = Stock(ticker, token=key)
        price = stock.get_price()[ticker].iloc[0]
    except:
        #print("Unexpected error:", sys.exc_info()[0])
        return {}

    if (sandbox):
        os.environ['IEX_API_VERSION'] = 'v1'
    return price


def getStockInfo(ticker, sandbox=False):
    """
    Fetches company info from stock ticker.

    Parameters
    ----------
    ticker      :string
    sandbox     :bool
                Sets the IEX environment to sandbox mode to make limitless API calls for testing.

    Returns
    -------
    dict object of 
    """
    #TODO: Go redo the iex package calls cause the maintainer changed all the shit to pandas output
    key = os.environ.get("IEX_TOKEN")
    if (sandbox):
        os.environ['IEX_API_VERSION'] = 'iexcloud-sandbox'
        key = os.environ.get("IEX_SANDBOX_TOKEN")
    try:
        stock = Stock(ticker, token=key)
        company = stock.get_company()
    except:
        #print("Unexpected error:", sys.exc_info()[0])
        return {}

    if (sandbox):
        os.environ['IEX_API_VERSION'] = 'v1'
    return company


def getHistoricalEarnings(ticker, quarters=4, sandbox=False):
    domain = 'cloud.iexapis.com'
    key = os.environ.get("IEX_TOKEN")
    if (sandbox):
        domain = 'sandbox.iexapis.com'
        key = os.environ.get("IEX_SANDBOX_TOKEN")
    try:
        url = 'https://{}/stable/stock/{}/earnings/{}/?token={}'.format(
            domain,
            ticker,
            quarters,
            key
        )
        earnings = requests.get(url).json()
    except:
        #print("Unexpected error:", sys.exc_info()[0])
        return None

    return earnings


def getPriceTarget(ticker, sandbox=False):
    domain = 'cloud.iexapis.com'
    key = os.environ.get("IEX_TOKEN")
    if (sandbox):
        domain = 'sandbox.iexapis.com'
        key = os.environ.get("IEX_SANDBOX_TOKEN")
    try:
        url = 'https://{}/stable/stock/{}/price-target?token={}'.format(
            domain,
            ticker,
            key
        )
        priceTarget = requests.get(url).json()
    except:
        #print("Unexpected error:", sys.exc_info()[0])
        return None

    return priceTarget


def getQuoteData(ticker, sandbox=False):
    key = os.environ.get("IEX_TOKEN")
    if (sandbox):
        os.environ['IEX_API_VERSION'] = 'iexcloud-sandbox'
        key = os.environ.get("IEX_SANDBOX_TOKEN")
    try:
        stock = Stock(ticker, token=key)
        quote = stock.get_quote()
    except:
        #print("Unexpected error:", sys.exc_info()[0])
        return {}
    if (sandbox):
        os.environ['IEX_API_VERSION'] = 'v1'
    return quote


def getKeyStats(ticker, filterResults=False, sandbox=False):
    domain = 'cloud.iexapis.com'
    key = os.environ.get("IEX_TOKEN")
    if (sandbox):
        domain = 'sandbox.iexapis.com'
        key = os.environ.get("IEX_SANDBOX_TOKEN")
    if (filterResults):
        filters = ",".join(filterResults)
    try:
        url = 'https://{}/stable/stock/{}/stats?token={}'.format(
            domain,
            ticker,
            key
        )
        if (filterResults):
            url = 'https://{}/stable/stock/{}/stats?filter={}&token={}'.format(
                domain,
                ticker,
                filters,
                key
            )
        keyStats = requests.get(url).json()
    except:
        #print("Unexpected error:", sys.exc_info()[0])
        return None

    return keyStats


def getAdvancedStats(ticker, filterResults=False, sandbox=False):
    domain = 'cloud.iexapis.com'
    key = os.environ.get("IEX_TOKEN")
    if (sandbox):
        domain = 'sandbox.iexapis.com'
        key = os.environ.get("IEX_SANDBOX_TOKEN")
    if (filterResults):
        filters = ",".join(filterResults)
    try:
        url = 'https://{}/stable/stock/{}/advanced-stats?token={}'.format(
            domain,
            ticker,
            key
        )
        if (filterResults):
            url = 'https://{}/stable/stock/{}/advanced-stats?filter={}&token={}'.format(
                domain,
                ticker,
                filters,
                key
            )
        advancedStats = requests.get(url).json()
    except:
        #print("Unexpected error:", sys.exc_info()[0])
        return None

    return advancedStats


def getFinancials(ticker, sandbox=False):
    domain = 'cloud.iexapis.com'
    key = os.environ.get("IEX_TOKEN")
    if (sandbox):
        domain = 'sandbox.iexapis.com'
        key = os.environ.get("IEX_SANDBOX_TOKEN")
    try:
        url = 'https://{}/stable/stock/{}/financials?token={}'.format(
            domain,
            ticker,
            key
        )
        financials = requests.get(url).json()
    except:
        # print("Unexpected error:", sys.exc_info()[0])
        return None

    return financials


def getCashFlow(ticker, sandbox=False):
    domain = 'cloud.iexapis.com'
    key = os.environ.get("IEX_TOKEN")
    if (sandbox):
        domain = 'sandbox.iexapis.com'
        key = os.environ.get("IEX_SANDBOX_TOKEN")
    try:
        url = 'https://{}/stable/stock/{}/cash-flow?token={}'.format(
            domain,
            ticker,
            key
        )
        cashflow = requests.get(url).json()
    except:
        # print("Unexpected error:", sys.exc_info()[0])
        return None

    return cashflow
    


def getHistoricalData(ticker, timeframe, priceOnly=False, sandbox=False):
    domain = 'cloud.iexapis.com'
    key = os.environ.get("IEX_TOKEN")
    if (sandbox):
        domain = 'sandbox.iexapis.com'
        key = os.environ.get("IEX_SANDBOX_TOKEN")
    try:
        url = 'https://{}/stable/stock/{}/chart/{}?token={}'.format(
            domain,
            ticker,
            timeframe,
            key
        )
        if (priceOnly):
            url = 'https://{}/stable/stock/{}/chart/{}?chartCloseOnly=true&token={}'.format(
                domain,
                ticker,
                timeframe,
                key
            )

        historicalData = requests.get(url).json()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return {}

    return historicalData


def batchHistoricalData(batch, timeframe, priceOnly=False, sandbox=False):
    domain = 'cloud.iexapis.com'
    key = os.environ.get("IEX_TOKEN")
    if (sandbox):
        domain = 'sandbox.iexapis.com'
        key = os.environ.get("IEX_SANDBOX_TOKEN")

    batch = ",".join(batch)  # Convert to comma-separated string
    try:
        url = 'https://{}/stable/stock/market/batch?symbols={}&types=chart&range={}&token={}'.format(
            domain,
            batch,
            timeframe,
            key
        )
        if (priceOnly):
            url = 'https://{}/stable/stock/market/batch?symbols={}&types=chart&range={}&chartCloseOnly=true&token={}'.format(
                domain,
                batch,
                timeframe,
                key
            )
        print(url)
        sys.exit()
        batchrequest = requests.get(url).json()
    except:
        # print("Unexpected error:", sys.exc_info()[0])
        return {}

    return batchrequest
