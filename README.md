Must have an IEX Console API token. Some commands will not work without a premium subscription.
https://iexcloud.io/


Check out the .env.example file. If you have a Twitter developer account, you can hook up your twitter to post the output.

Make sure to run ```pip list -r requirements.txt```

DEBUG=on
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

Run this command to view available commands. All commands must be prepended with python run.py.

(Apologies if a few are broken. This is a sort of playground of mine and I'm constantly changing/adding new things.

```python run.py list```
