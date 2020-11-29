from django.contrib import admin
from .models import *

admin.site.register(Stock)
admin.site.register(MacroTrend)
admin.site.register(Watchlist)
admin.site.register(Earnings)
admin.site.register(Trend)
admin.site.register(Vol)
admin.site.register(Financials)
admin.site.register(HistoricalPrices)