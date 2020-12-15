from flask import Flask, Blueprint
from .nbp_data import manage_db_data
from .routes.rates import rates
from .routes.sales import sales
from api.constants import CACHE_UPDATE
import api.cache
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

def create_app(conf):
    app = Flask(__name__)

    config.limiter.init_app(app)
    app.config.from_object(conf)
    caches = manage_db_data()
    cache.sales_cache = caches[0]
    cache.sales_cache_usd = caches[1]
    app.register_blueprint(rates)
    app.register_blueprint(sales)

    cron = BackgroundScheduler()
    cron.add_job(cache.update_cache_data, 'interval', hours=CACHE_UPDATE, max_instances=1)
    cron.start()
    atexit.register(lambda: cron.shutdown(wait=False))
    
    return app
