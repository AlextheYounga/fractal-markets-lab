import django
from django.apps import apps
from ..core.functions import extract_data, chunks
from ..core.output import printFullTable, writeCSV
from ..core.api import getHistoricalData
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import json
import sys
import os
from dotenv import load_dotenv
load_dotenv()
django.setup()


# TODO: Figure out single comparisons
def compare(t1, t2 ,timespan='5y', sandbox=True):
    for t in [t1, t2]:

