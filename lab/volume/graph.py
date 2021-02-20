from dotenv import load_dotenv
import json
import sys
import redis
import time
from datetime import date
from ..redisdb.controller import rdb_save_stock
from ..core.api.historical import getHistoricalData
from ..core.output import printFullTable, writeCSV
from ..fintwit.tweet import send_tweet
load_dotenv()

def graph_volume(ticker, timeframe='3m', sandbox=False):
    hdata = getHistoricalData(ticker, timeframe=timeframe, sandbox=sandbox)
    print(json.dumps(hdata, indent=1))