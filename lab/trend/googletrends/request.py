from pytrends.request import TrendReq

pytrends = TrendReq(hl='en-US', tz=360)
kw_list = ["gsat stock"]
pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')
interest = pytrends.interest_over_time()

print(interest)