import os
import json
from iexfinance.stocks import Stock

# print(json.dumps(os.environ, indent=1))
print(os.environ)
print(os.environ.get('IEX_TOKEN'))
print(os.getenv('IEX_TOKEN'))
# tsla = Stock('TSLA', token=os.environ.get('IEX_TOKEN'))
# tsla.get_price()