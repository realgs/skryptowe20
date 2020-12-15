from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(key_func=get_remote_address, application_limits=["1000/day", "400/hour"])

class BaseConf(object):
    ORIGINS = ["*"]

class DevelopmentConf(BaseConf):
    DEBUG = False
    TESTING = False
    ENV = "development"
    APPNAME = "salesAPI"
