from flask import Flask
from flask_mongoengine import MongoEngine
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from mongoengine import *

db = MongoEngine()

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'currency-and-sales',
    'host': "mongodb+srv://Skryptowe:yArfxRUIvpFQii7p@cluster0.gcuoh.mongodb.net/currency-and-sales?retryWrites=true"
            "&w=majority "
}
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour, 1/second"]
)
db.init_app(app)


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
