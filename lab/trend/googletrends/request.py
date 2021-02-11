from pytrends.request import TrendReq


def stock_search_trends(ticker):
    pytrends = TrendReq(hl='en-US', tz=360)
    kw_list = [ticker+' stock']
    pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')
    interest = pytrends.interest_over_time()

    print(interest)