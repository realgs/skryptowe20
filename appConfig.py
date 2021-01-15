from flask import Flask
from flask_mongoengine import MongoEngine
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache

db = MongoEngine()

app = Flask(__name__)
config = {
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 300
}
app.config.from_mapping(config)
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
cache = Cache(app)
