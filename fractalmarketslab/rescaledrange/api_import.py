from ..key import IEX_TOKEN
import json
from iexfinance.stocks import Stock


tsla = Stock('TSLA', token=IEX_TOKEN)
print(tsla.get_price())