Must have an IEX Console API token. Some commands will not work without a premium subscription.
https://iexcloud.io/



Make sure to run ```pip list -r requirements.txt```

Check out the .env.example file. If you have a Twitter developer account, you can hook up your twitter to post the output.


```
DJANGO_SETTINGS_MODULE='lab.settings'
DJANGO_SETTINGS_MODULE=lab.settings
IEX_TOKEN=pk_somevalue
IEX_SANDBOX_TOKEN=Tpk_somevalue
IEX_URL=https://cloud.iexapis.com/v1/
IEX_SANDBOX_URL=https://sandbox.iexapis.com/v1/
TWITTER_API_KEY='somevalue'
TWITTER_SECRET_KEY='somevalue'
TWITTER_ACCESS_KEY='somevalue'
TWITTER_ACCESS_SECRET='somevalue'
TWITTER_BEARER_TOKEN='somevalue'
```

Run this command to view available commands. All commands must be prepended with python run.py.

(Apologies if a few of these commands are broken. This is a sort of playground of mine and I'm constantly changing/adding new things.

```python run.py list```

```
Command                               Description
------------------------------------  ----------------------------------------------------------------------------------------------------------------
correlations:scan                     Runs correlations on all ETFs on the market, with *every other ETF on the market. (Takes about half an hour)
donchian [ticker]                     Runs a donchian range calculation on a ticker
financials [ticker]                   Returns financials data for ticker, including some custom indicators not provided by IEX.
macro:trends [timeperiod] [gain]      Scans all ETFs and returns the ETFs with the performance above an int (gain) within a timerange (5d, 1m, 3m, 1y)
macro:gainers                         Scans all ETFs and returns ETFs with highest day change.
hurst [ticker]                        Runs a rescaled range analysis on a ticker.
range [ticker]                        Runs a volatility range analysis on a ticker.
trend:chase                           Scans all stocks and returns todays gainers with above certain thresholds (weeds out the penny stocks).
trend:search [string]                 Scans stocks with string in stock name and looks for gainers
trend:earnings                        Scans all stocks and returns todays gainers who have consistently good earnings.
trend:volume                          Scans all stocks and returns todays gainers with abnormally high volume.
trend:gainers                         Grabs todays gainers and checks their earnings.
vix [ticker]                          Runs the VIX volatility equation on a ticker
```
