import django
from django.apps import apps
import json
import sys
from .methodology import sectors
from ..database.hp.update_prices import batch_refresh_prices
django.setup()

def refresh_sector_prices():
    batch_refresh_prices(batch=sectors(), timeframe='max')

