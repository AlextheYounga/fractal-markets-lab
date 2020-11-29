from ..core.api import getCashFlow, getFinancials, getKeyStats, getAdvancedStats, getCurrentPrice
from ..core.output import printTable
from ..core.functions import dataSanityCheck
import django
from django.apps import apps
import json
import sys
from dotenv import load_dotenv
load_dotenv()
django.setup()


def lookupFinancials(ticker):

    cash_flow_json = getCashFlow(ticker)
    financials_json = getFinancials(ticker)
    stats = getKeyStats(ticker, filterResults=['sharesOutstanding', 'peRatio'])
    advanced_stats = getAdvancedStats(ticker, filterResults=['priceToSales', 'EBITDA', 'debtToEquity'])
    price = getCurrentPrice(ticker)
    if (None not in [cash_flow_json, financials_json, stats, advanced_stats, price]):
        financials = financials_json['financials'][0]
        cash_flow = cash_flow_json['cashflow'][0]

        capitalExpenditures = dataSanityCheck(cash_flow, 'capitalExpenditures')
        sharesOutstanding = dataSanityCheck(stats, 'sharesOutstanding')
        shareholderEquity = dataSanityCheck(financials, 'shareholderEquity')
        cashFlow = dataSanityCheck(cash_flow, 'cashFlow')
        longTermDebt = dataSanityCheck(financials, 'longTermDebt')
        totalAssets = dataSanityCheck(financials, 'totalAssets')
        totalLiabilities = dataSanityCheck(financials, 'totalLiabilities')

        freeCashFlow = capitalExpenditures - cashFlow if (capitalExpenditures and cashFlow) else 0
        freeCashFlowPerShare = freeCashFlow / sharesOutstanding if (freeCashFlow and sharesOutstanding) else 0
        freeCashFlowYield = freeCashFlowPerShare / price if (freeCashFlowPerShare and price) else 0
        longTermDebtToEquity = longTermDebt / shareholderEquity if (longTermDebt and shareholderEquity) else 0
        netWorth = totalAssets - totalLiabilities if (totalAssets and totalLiabilities) else 0

        financialData = {
            'ticker': ticker,
            'reportDate': financials['reportDate'],
            'netIncome': financials['netIncome'],
            'netWorth': netWorth,
            'shortTermDebt': financials['shortTermDebt'],
            'longTermDebt': financials['longTermDebt'],
            'totalCash': financials['totalCash'],
            'totalDebt': financials['totalDebt'],
            'debtToEquity': advanced_stats['debtToEquity'],
            'priceToSales': advanced_stats['priceToSales'],
            'EBITDA': advanced_stats['EBITDA'],
            'freeCashFlow': freeCashFlow,
            'freeCashFlowPerShare': freeCashFlowPerShare,
            'freeCashFlowYield': freeCashFlowYield,
            'longTermDebtToEquity': longTermDebtToEquity,
        }
        printTable(financialData)

        Stock = apps.get_model('database', 'Stock')
        Financials = apps.get_model('database', 'Financials')

        del financialData['ticker']
        stock, created = Stock.objects.update_or_create(
            ticker=ticker,
            defaults={'lastPrice': price},
        )

        
        Financials.objects.update_or_create(
            stock=stock,
            defaults=financialData,
        )
    else:
        print('Could not fetch financials')
