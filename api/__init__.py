from flask import Flask, Blueprint
from .nbp_data import manage_db_data
from .routes.rates import rates

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    manage_db_data()
    app.register_blueprint(rates)
    return app