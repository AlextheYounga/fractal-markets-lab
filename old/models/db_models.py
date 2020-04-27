# from django.db import models
# from jsonfield import JSONField

# Create your models here.
class Asset(models.Model):
    name = models.CharField(max_length=900)
    ticker = models.CharField(max_length=10, null=True, blank=True)
    last_price = models.FloatField(null=True, blank=True)

class Vol(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    asset_name = models.CharField(max_length=900, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    open_price = models.FloatField(null=True, blank=True)
    close_price = models.FloatField(null=True, blank=True)
    log_returns = models.FloatField(null=True, blank=True)
    low = models.FloatField(null=True, blank=True)
    high = models.FloatField(null=True, blank=True)
    low_rr = models.FloatField(null=True, blank=True)
    high_rr = models.FloatField(null=True, blank=True)    
    volatility_index = models.FloatField(null=True, blank=True)
    volume = models.FloatField(null=True, blank=True)
    put_call_ratio = models.FloatField(null=True, blank=True)
    vol_stats = JSONField()