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


def quoteStatsBatchRequest(batch):
    # Accepts list of tickers
    # Maximum 100

    batch = ",".join(batch)  # Convert to comma-separated string
    try:
        url = 'https://cloud.iexapis.com/stable/stock/market/batch?symbols={}&types=quote,stats&token={}'.format(batch, os.environ.get("IEX_TOKEN"))
        batch_request = requests.get(url).json()
    except:
        #print("Unexpected error:", sys.exc_info()[0])
        return {}

    return batch_request


def companyBatchRequest(batch):
    # Accepts list of tickers
    # Maximum 100
    try:
        batch = ",".join(batch)  # Convert to comma-separated string
        url = 'https://cloud.iexapis.com/stable/stock/market/batch?symbols={}&types=quote,company&token={}'.format(batch, os.environ.get("IEX_TOKEN"))
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


def getEarnings(ticker):
    try:
        url = 'https://cloud.iexapis.com/stable/stock/{}/earnings/4/?token={}'.format(ticker, os.environ.get("IEX_TOKEN"))
        earnings = requests.get(url).json()
    except:
        #print("Unexpected error:", sys.exc_info()[0])
        return None

    return earnings


def getPriceTarget(ticker):
    try:
        url = 'https://cloud.iexapis.com/stable/stock/{}/price-target?token={}'.format(ticker, os.environ.get("IEX_TOKEN"))
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


def getHistoricalData(ticker, timeframe, priceOnly=False):
    try:
        url = 'https://cloud.iexapis.com/stable/stock/{}/chart/{}?token={}'.format(
            ticker,
            timeframe,
            os.environ.get("IEX_TOKEN")
        )
        if (priceOnly):
            url = 'https://cloud.iexapis.com/stable/stock/{}/chart/{}?chartCloseOnly=true&token={}'.format(
                ticker,
                timeframe,
                os.environ.get("IEX_TOKEN")
            )
        historicalData = requests.get(url).json()
    except:
        #print("Unexpected error:", sys.exc_info()[0])
        return {}

    return historicalData

# ----------------------------------------------
# Testing Queries using IEX Sandbox
# ----------------------------------------------

def testHistoricalData(ticker, timeframe, priceOnly=False):
    try:
        url = 'https://sandbox.iexapis.com/stable/stock/{}/chart/{}?token={}'.format(
            ticker,
            timeframe,
            os.environ.get("IEX_SANDBOX_TOKEN")
        )
        if (priceOnly):
            url = 'https://sandbox.iexapis.com/stable/stock/{}/chart/{}?chartCloseOnly=true&token={}'.format(
                ticker,
                timeframe,
                os.environ.get("IEX_SANDBOX_TOKEN")
            )

        historicalData = requests.get(url).json()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return {}

    return historicalData
