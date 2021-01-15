from mongoengine import *


class Exchange(Document):
    code = StringField(max_length=3)
    dateStr = StringField()
    date = DateField()
    mid = FloatField()
    interpolated = BooleanField()


class SalesResult(Document):
    dateStr = StringField()
    date = DateField()
    usd = FloatField()
    pln = FloatField()
