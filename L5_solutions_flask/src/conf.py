import os

DB_NAME = 'Northwind_large.sqlite'
PATH_TO_DB = os.path.normpath(os.path.join(os.path.dirname(__file__), os.path.pardir, DB_NAME))
DEFAULT_LIMIT = "10/s"
DEFAULT_CACHE_TIMEOUT = 100
