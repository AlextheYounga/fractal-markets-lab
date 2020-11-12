import django
from ..core.api import getCurrentPrice
from django.apps import apps
import requests
import json
import sys
import os
from dotenv import load_dotenv
load_dotenv()
django.setup()


def dynamicUpdateCreate(data, find):
    """ 
    Parameters
    ----------
    data :  dict
            Data must conform to this structure:
                data = {
                    'Model': {
                    'column': value
                    },
                }
    find :  QuerySet object

    Returns
    -------
    boolean|string
    """
    if (isinstance(data, dict)):
        for model, values in data.items():
            Model = apps.get_model('database', model)
            Model.objects.update_or_create(
                stock=find,
                defaults=values,
            )
    else:
        return 'Data must be in dict structure'

    return True


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
