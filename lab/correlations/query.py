import django
from django.apps import apps
from ..core.functions import extract_data, chunks
from ..core.output import printFullTable, writeCSV
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import json
import sys
import os
from dotenv import load_dotenv
load_dotenv()
django.setup()



