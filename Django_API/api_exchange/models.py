from django.db import models


# Create your models here.
class ExchangeRate(models.Model):
    date = models.DateField()
    rate = models.DecimalField(decimal_places=4, max_digits=10)
    interpolated = models.BooleanField(default=False)
    volumePLN = models.DecimalField(decimal_places=4, max_digits=14)
    volumeUSD = models.DecimalField(decimal_places=4, max_digits=14)

    def __str__(self):
        return 'Date: {0}, Rate: {1}'.format(self.date, self.rate)
