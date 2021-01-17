DATABASE_FILE_PATH = 'database.sqlite'
DEBUG_MODE = True  # [True | False]
FRONT_ADDRESS = '127.0.0.1'

######## LIMITER #####################
ENABLE_LIMITER = True  # [True | False]
INDEX_LIMIT = '10000 per hour'
GET_RATES_ALL_LIMIT = '5 per minute;50 per hour'
GET_RATE_DAY_LIMIT = '100 per minute;1000 per hour'
GET_RATES_RANGE_LIMIT = '10 per minute;100 per hour'
GET_SALES_SUM_DAY_LIMIT = '100 per minute;1000 per hour'

# Rate limit string notation https://flask-limiter.readthedocs.io/en/stable/#rate-limit-string-notation
