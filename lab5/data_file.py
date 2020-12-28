# database boundaries
DATABASE_DATE_FROM = "2011-10-01"
DATABASE_DATE_TO = "2014-05-28"
AVAILABLE_CURRENCIES = ['AUD', 'BYN', 'BGN', 'HRK', 'DKK',
                        'JPY', 'CAD', 'NOK', 'CZK', 'RUB',
                        'RON', 'PLN', 'CHF', 'SEK', 'TRY',
                        'EUR', 'UAH', 'HUF', 'GBP']

# database data
SALES_DATABASE = 'AdventureWorks2019'
SALES_TABLE_NAME = 'Sales.SalesOrderHeader'
CURRENCY_TABLE_NAME = 'Sales.CurrencyRatesTable'
DAILY_SALES_TABLE_NAME = 'Sales.DailySalesTable'
SERVER = 'DESKTOP-1A5C2CG'

# api app data
CACHE_TYPE = "simple"
CACHE_TIMEOUT = 6000
DEFAULT_LIMIT = "20 per minutes"

# nbp api data
NBP_API_URL = 'http://api.nbp.pl/api/exchangerates/rates/'
MAX_DAYS_AMOUNT = 365
