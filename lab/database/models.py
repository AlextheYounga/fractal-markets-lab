from django.db import models
from jsonfield import JSONField
# from bulk_update_or_create import BulkUpdateOrCreateQuerySet

# Create your models here.
class Stock(models.Model):
    ticker = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=200)
    lastPrice = models.FloatField(null=True)
    sector = models.CharField(max_length=300, null=True)
    industry = models.CharField(max_length=300, null=True)
    employees = models.IntegerField(null=True)
    description = models.TextField(null=True)
    index = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Watchlist(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, default=0)
    ticker = models.CharField(max_length=30)
    name = models.CharField(max_length=200)
    lastPrice = models.FloatField(null=True)
    peRatio = JSONField(null=True)
    week52 = models.FloatField(null=True)
    day5ChangePercent = models.FloatField(null=True)
    month1ChangePercent = models.FloatField(null=True)
    ytdChangePercent = models.FloatField(null=True)
    day50MovingAvg = models.FloatField(null=True)
    day200MovingAvg = models.FloatField(null=True)
    fromHigh = models.FloatField(null=True)
    reportedEPS = JSONField(null=True)
    reportedConsensus = JSONField(null=True)
    ttmEPS = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Portfolio(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, default=0)
    ticker = models.CharField(max_length=30)
    name = models.CharField(max_length=200)
    purchase_price = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):              # __str__ on Python 3
        return str(self.about_desc)

    class Meta:
        verbose_name_plural = "portfolio"


class Earnings(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    reportedEPS = JSONField(null=True)
    reportedConsensus = JSONField(null=True)
    ttmEPS = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):              # __str__ on Python 3
        return str(self.about_desc)

    class Meta:
        verbose_name_plural = "earnings"


class Valuation(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    peRatio = JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Trend(models.Model):

    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    week52 = models.FloatField(null=True)
    day5ChangePercent = models.FloatField(null=True)
    month1ChangePercent = models.FloatField(null=True)
    ytdChangePercent = models.FloatField(null=True)
    day50MovingAvg = models.FloatField(null=True)
    day200MovingAvg = models.FloatField(null=True)
    fromHigh = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Vol(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    lowerRange = models.FloatField(null=True)
    upperRange = models.FloatField(null=True)
    lowerStDev = models.FloatField(null=True)
    upperStDev = models.FloatField(null=True)
    technicalLow = models.FloatField(null=True)
    technicalHigh = models.FloatField(null=True)
    week3DonchianLow = models.FloatField(null=True)
    week3DonchianHigh = models.FloatField(null=True)
    stDev = models.FloatField(null=True)
    stDevPercent = models.CharField(max_length=200, null=True)
    volumeChange = models.CharField(max_length=200, null=True)
    percentUpside = models.CharField(max_length=200, null=True)
    percentDownside = models.CharField(max_length=200, null=True)
    month3Trend = models.CharField(max_length=200, null=True)
    signal = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):              # __str__ on Python 3
        return str(self.about_desc)

    class Meta:
        verbose_name_plural = "vol"
