import statistics
import json
import os
import sys
from .functions import *
from ..shared.functions import *
from ..shared.api import getQuoteData
from ..shared.imports import parseCSV
from tabulate import tabulate

nasdaq = parseCSV('NasdaqComposite.csv')
