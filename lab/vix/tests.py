from ..core.api.options import getExpirations
from ..core.api.stats import getKeyStats
from .functions import optionExpirationMinutes

# print(optionExpirationMinutes)
# print(optionExpirationMinutes('SPY'))
print(getKeyStats('SPY', filterResults=['beta']))