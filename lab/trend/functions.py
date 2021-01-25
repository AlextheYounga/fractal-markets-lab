import django
from ..core.api import getCurrentPrice
from django.apps import apps
import requests
import json
import sys
from dotenv import load_dotenv
load_dotenv()
django.setup()


def checkEarnings(earnings):
    actual = []
    consensus = []
    consistency = []

    if (len(earnings['earnings']) > 1):
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
