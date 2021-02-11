from dotenv import load_dotenv
import json
import sys
import redis
import time
from datetime import date
from ..redisdb.controller import rdb_save_stock
from ..core.api import quoteStatsBatchRequest, getPriceTarget
from ..core.output import printFullTable, writeCSV
from ..fintwit.tweet import send_tweet
load_dotenv()