import django
from django.apps import apps
import json
import sys
import os
from dotenv import load_dotenv
from ..twitter.tweet import send_tweet
load_dotenv()
django.setup()