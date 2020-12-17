from django.db import models


class Currency(models.Model):
    symbol = models.CharField(max_length=3, blank=False, default='')
    date = models.DateTimeField()
    value = models.FloatField()
    interpolated = models.BooleanField(default='False')

    class Meta:
        unique_together = (("symbol", "date"),)
        ordering = ('date',)


class SalesStats(models.Model):
    date = models.DateTimeField(primary_key=True)
    sales_sum = models.FloatField()

    class Meta:
        ordering = ('date',)


# Create your models here.
