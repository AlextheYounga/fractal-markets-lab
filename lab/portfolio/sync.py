import django
from django.apps import apps
from os import listdir
from os.path import isfile, join
import json
import sys
from .functions import *
from ..core.functions import *
from ..core.export import writeCSV
django.setup()

PORTFOLIO = 'lab/core/storage/portfolio/'
files = [f for f in listdir(PORTFOLIO) if isfile(join(PORTFOLIO, f))]
files.remove('.DS_Store')
last = latestFile(files)

portfolio = parsePortfolioCSV(last)
print(json.dumps(portfolio, indent=1))
