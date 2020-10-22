from django.db import models

# Create your models here.
class Index(models.Model):
    name = models.CharField(max_length=200, unique=True)
    count = models.IntegerField(null=True)

    def __unicode__(self):              # __str__ on Python 3
        return str(self.about_desc)

    class Meta:
        verbose_name_plural = "indices"


class Stock(models.Model):
    index_id = models.ForeignKey(Index, on_delete=models.CASCADE, default=0)
    ticker = models.CharField(max_length=30)
    name = models.CharField(max_length=200)
    lastPrice = models.IntegerField(null=True)


class Earnings(models.Model):
    stock_id = models.ForeignKey(Stock, on_delete=models.CASCADE)
    lastEPS = models.IntegerField(null=True)
    consensusEPS = models.IntegerField(null=True)
    trailingEPS = models.IntegerField(null=True)

    def __unicode__(self):              # __str__ on Python 3
        return str(self.about_desc)

    class Meta:
        verbose_name_plural = "earnings"


class Trend(models.Model):
    stock_id = models.ForeignKey(Stock, on_delete=models.CASCADE)
    week52 = models.IntegerField(null=True)
    day5ChangePercent = models.IntegerField(null=True)
    month1ChangePercent = models.IntegerField(null=True)
    day50MovingAvg = models.IntegerField(null=True)
    day200MovingAvg = models.IntegerField(null=True)
    fromHigh = models.IntegerField(null=True)


class Vol(models.Model):
    stock_id = models.ForeignKey(Stock, on_delete=models.CASCADE)
    lowerRange = models.IntegerField(null=True)
    upperRange = models.IntegerField(null=True)
    lowerStDev = models.IntegerField(null=True)
    upperStDev = models.IntegerField(null=True)
    technicalLow = models.IntegerField(null=True)
    technicalHigh = models.IntegerField(null=True)
    week3DonchianLow = models.IntegerField(null=True)
    week3DonchianHigh = models.IntegerField(null=True)
    stDev = models.IntegerField(null=True)
    stDevPercent = models.CharField(max_length=200, null=True)
    volumeChange = models.CharField(max_length=200, null=True)
    percentUpside = models.CharField(max_length=200, null=True)
    percentDownside = models.CharField(max_length=200, null=True)
    month3Trend = models.CharField(max_length=200, null=True)
    signal = models.CharField(max_length=200, null=True)

    def __unicode__(self):              # __str__ on Python 3
        return str(self.about_desc)

    class Meta:
        verbose_name_plural = "vol"
