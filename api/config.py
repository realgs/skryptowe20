import os


class BaseConf(object):
    ORIGINS = ["*"]

class DevelopmentConf(BaseConf):
    DEBUG = True
    TESTING = False
    ENV = "development"
    APPNAME = "salesAPI"
    