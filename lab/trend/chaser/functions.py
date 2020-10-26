import django
from ...core.api import getCurrentPrice
from django.apps import apps
import requests
import json
import sys
import os
from dotenv import load_dotenv
load_dotenv()
django.setup()



def getTrendData(ticker):
    try:
        price = getCurrentPrice(ticker)
        url = 'https://cloud.iexapis.com/stable/stock/{}/stats?token={}'.format(ticker, os.environ.get("IEX_TOKEN"))
        stats = requests.get(url).json()

        return price, stats
    except:
        return None, None



def getEarnings(ticker):
    try:
        url = 'https://cloud.iexapis.com/stable/stock/{}/earnings/4/?token={}'.format(ticker, os.environ.get("IEX_TOKEN"))
        earnings = requests.get(url).json()
    except:
        return None

    return earnings



def checkEarnings(earnings):    
    actual = []
    consensus = []
    consistency = []

    for i, report in enumerate(earnings['earnings']):
        actualEps = report['actualEPS'] if 'actualEPS' in report else 0
        surpriseEps = report['EPSSurpriseDollar'] if 'EPSSurpriseDollar' in report else 0
        if (i + 1 in range(-len(earnings['earnings']), len(earnings['earnings']))):
            previous = earnings['earnings'][i + 1]['actualEPS']
            greater = actualEps > previous
            consistency.append(greater)

        period = report['fiscalPeriod'] if 'fiscalPeriod' in report else i
        actual.append({period: actualEps})
        consensus.append({period: surpriseEps})
        
    improvement = False if False in consistency else True

    results = {
        'actual': actual,
        'consensus': consensus,
        'improvement': improvement,
    }

    return results



