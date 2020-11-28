from iexfinance.stocks import get_historical_data
from iexfinance.stocks import Stock
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests
import sys
import json
import csv
import os
load_dotenv()


def syncStocks():
    try:
        url = 'https://cloud.iexapis.com/stable/ref-data/iex/symbols?token={}'.format(os.environ.get("IEX_TOKEN"))
        tickers = requests.get(url).json()
    except:
        #print("Unexpected error:", sys.exc_info()[0])
        return {}

    return tickers


def quoteStatsBatchRequest(batch, sandbox=False):
    # Accepts list of tickers
    # Maximum 100
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
    # Accepts list of tickers
    # Maximum 100
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


def getCurrentPrice(ticker):
    try:
        stock = Stock(ticker, token=os.environ.get("IEX_TOKEN"))
        price = stock.get_price()
    except:
        #print("Unexpected error:", sys.exc_info()[0])
        return {}

    return price


def getStockInfo(ticker):
    try:
        stock = Stock(ticker, token=os.environ.get("IEX_TOKEN"))
        company = stock.get_company()
    except:
        #print("Unexpected error:", sys.exc_info()[0])
        return {}

    return company


def getEarnings(ticker, sandbox=False):
    domain = 'cloud.iexapis.com'
    key = os.environ.get("IEX_TOKEN")
    if (sandbox):
        domain = 'sandbox.iexapis.com'
        key = os.environ.get("IEX_SANDBOX_TOKEN")
    try:
        url = 'https://{}/stable/stock/{}/earnings/4/?token={}'.format(
            domain,
            ticker,
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


def getQuoteData(ticker):
    try:
        stock = Stock(ticker, token=os.environ.get("IEX_TOKEN"))
        quote = stock.get_quote()
    except:
        #print("Unexpected error:", sys.exc_info()[0])
        return {}

    return quote


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
        #print("Unexpected error:", sys.exc_info()[0])
        return {}

    return historicalData

