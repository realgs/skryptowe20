from enum import Enum
from datetime import datetime


class Currency(Enum):
    USD = 'USD'
    EUR = 'EUR'
    CHF = 'CHF'
    PLN = 'PLN'


REQUEST_LIMIT = 366
FIRST_DAY = datetime.strptime('2002-01-02', '%Y-%m-%d')
LAST_DAY = datetime.strptime('2020-12-17', '%Y-%m-%d')
FIRST_DAY_SALES = datetime.strptime('2003-01-06', '%Y-%m-%d')
LAST_DAY_SALES = datetime.strptime('2005-05-31', '%Y-%m-%d')
