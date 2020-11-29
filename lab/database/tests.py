import django
from django.apps import apps
from dotenv import load_dotenv
import json
import os
import sys
from datetime import date
from .functions import *
from ..core.api import getHistoricalData
import texttable
load_dotenv()
django.setup()

prices = getHistoricalData('TSLA', '3m')
saveHistoricalPrices('TSLA', prices)