from django.db import models

class DailySales(models.Model):
    sales_id = models.AutoField(primary_key=True, blank=True)
    salesdate = models.TextField(blank=True, null=True)
    plnsales = models.IntegerField(blank=True, null=True)
    usdsales = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.sales_id)+'/'+str(self.salesdate)+'/'+str(self.plnsales)+'/'+str(self.usdsales)
    class Meta:
        managed = False
        db_table = 'DailySales'


class SalesOrders(models.Model):
    orderdate = models.TextField(db_column='OrderDate', blank=True, null=True)  
    orderid = models.TextField(db_column='OrderID', blank=True, primary_key=True)
    totaldue = models.TextField(db_column='TotalDue', blank=True, null=True)

    
    def __str__(self):
        return str(self.orderdate)+'/'+str(self.orderid)+'/'+str(self.totaldue)
    class Meta:
        managed = False
        db_table = 'SalesOrders'

class CurrencyRecord(models.Model):
    id = models.IntegerField(db_column='ID', blank=True, primary_key=True)
    effectivedate = models.TextField(db_column='EffectiveDate', blank=True, null=True)
    currencyvalue = models.FloatField(db_column='CurrencyValue', blank=True, null=True)
    interpolated = models.IntegerField(db_column='Interpolated', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'UsdToPlnInter'
