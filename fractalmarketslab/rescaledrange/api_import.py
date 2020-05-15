import os
from iexfinance.stocks import Stock


tsla = Stock('TSLA', token=os.environ.get('IEX_TOKEN'))
tsla.get_price()