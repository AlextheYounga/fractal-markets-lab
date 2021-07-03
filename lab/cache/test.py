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
}
    
EasyCache.get('test.data.chain')
