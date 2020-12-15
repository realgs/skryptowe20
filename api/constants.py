from enum import Enum

REQUEST_DAYS_LIMIT = 367
DATE_FORMAT = "%Y-%m-%d"
DB_DATE_FORMAT = "%m/%d/%Y"
YEARS = [2004, 2005]
CACHE_UPDATE=24
MAX_LAST_REQUEST = 100
REQUEST_LIMIT = '200/day;30/minute'

class Currencies(Enum):
    USD = 'usd'
    CHF = 'chf'
    EUR = 'eur'
    