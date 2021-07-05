from .easy_cache import EasyCache
import json

data = {
  "symbol": "SPY",
  "status": "SUCCESS",
  "underlying": None,
  "strategy": "SINGLE",
  "interval": 0,
  "isDelayed": True,
  "isIndex": False,
  "interestRate": 0.1,
  "underlyingPrice": 388.245,
  "volatility": 29,
  "daysToExpiration": 0,
  "numberOfContracts": 4502,
  "1symbol": "SPY",
  "1status": "SUCCESS",
  "1underlying": None,
  "1strategy": "SINGLE",
  "1interval": 0,
  "1isDelayed": True,
  "1isIndex": False,
  "1interestRate": 0.1,
  "1underlyingPrice": 388.245,
  "1volatility": 29,
  "1daysToExpiration": 0,
  "1numberOfContracts": 4502,
}
# JSON = 'lab/vix/sample_response/response.json'
# with open(JSON) as jsonfile:
#     chain = json.loads(jsonfile.read())

# data = 'This is a test'

# print()

# EasyCache.put('test.data.string', data)
print(EasyCache.get('test.data.string'))
