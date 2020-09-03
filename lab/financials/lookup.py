import json
from ..shared.functions import *
from ..shared.imports import *
from tabulate import tabulate
import requests
import json
import csv
import os
import sys
from dotenv import load_dotenv
load_dotenv()


def lookupFinancials(ticker):
    # get_cash_flow = 'https://sandbox.iexapis.com/v1/stock/{}/cash-flow?token={}'.format(ticker, os.environ.get('IEX_SANDBOX_TOKEN'))
    # get_financials = 'https://sandbox.iexapis.com/v1/stock/{}/financials?token={}'.format(ticker, os.environ.get('IEX_SANDBOX_TOKEN'))
    # get_stats = 'https://sandbox.iexapis.com/v1/stock/{}/stats?filter=sharesOutstanding&token={}'.format(ticker, os.environ.get('IEX_SANDBOX_TOKEN'))
    get_cash_flow = 'https://cloud.iexapis.com/v1/stock/{}/cash-flow?token={}'.format(ticker, os.environ.get('IEX_TOKEN'))
    get_financials = 'https://cloud.iexapis.com/v1/stock/{}/financials?token={}'.format(ticker, os.environ.get('IEX_TOKEN'))
    get_stats = 'https://cloud.iexapis.com/v1/stock/{}/stats?filter=sharesOutstanding&token={}'.format(ticker, os.environ.get('IEX_TOKEN'))

    financials_json = requests.get(get_financials).json()
    cash_flow_json = requests.get(get_cash_flow).json()
    stats = requests.get(get_stats).json()
    price = getCurrentPrice(ticker)

    financials = financials_json['financials'][0]
    cash_flow = cash_flow_json['cashflow'][0]

    capitalExpenditures = cash_flow['capitalExpenditures'] if ('capitalExpenditures' in cash_flow) else 0
    sharesOutstanding = stats['sharesOutstanding'] if ('sharesOutstanding' in stats) else 0
    shareholderEquity = financials['shareholderEquity'] if ('shareholderEquity' in financials) else 0
    cashFlow = cash_flow['cashFlow'] if ('cashFlow' in cash_flow) else 0
    longTermDebt = financials['longTermDebt'] if ('longTermDebt' in financials) else 0

    freeCashFlow = capitalExpenditures - cashFlow if (capitalExpenditures and cashFlow) else 0
    freeCashFlowPerShare = freeCashFlow / sharesOutstanding if (freeCashFlow and sharesOutstanding) else 0
    freeCashFlowYield = freeCashFlowPerShare / price if (freeCashFlowPerShare and price) else 0
    longTermDebtToEquity = longTermDebt / shareholderEquity if (longTermDebt and shareholderEquity) else 0

    print(tabulate([
        ['reportDate', financials['reportDate']],
        ['shareholderEquity', financials['shareholderEquity']],
        ['grossProfit', financials['grossProfit']],
        ['totalRevenue', financials['totalRevenue']],
        ['netIncome', financials['netIncome']],
        ['totalAssets', financials['totalAssets']],
        ['totalLiabilities', financials['totalLiabilities']],
        ['shortTermDebt', financials['shortTermDebt']],
        ['longTermDebt', financials['longTermDebt']],
        ['totalCash', financials['totalCash']],
        ['totalDebt', financials['totalDebt']],
        ['freeCashFlow', freeCashFlow],
        ['freeCashFlowPerShare', freeCashFlowPerShare],
        ['freeCashFlowYield', freeCashFlowYield],
        ['longTermDebtToEquity', longTermDebtToEquity]],
        headers=[ticker]))

    return "\nDone"
