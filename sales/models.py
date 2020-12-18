from django.db import models


class Currency(models.Model):
    symbol = models.CharField(max_length=3, blank=False, default='')
    date = models.DateField()
    value = models.FloatField()
    interpolated = models.BooleanField(default='False')

    class Meta:
        unique_together = (("symbol", "date"),)
        ordering = ('date',)


class SalesStats(models.Model):
    date = models.DateField(primary_key=True)
    sales_sum = models.FloatField()
    usd = models.FloatField()
    eur = models.FloatField()

    class Meta:
        ordering = ('date',)


# Create your models here.
