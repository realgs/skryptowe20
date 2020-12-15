from api.manage_db import get_transaction_sums_for_days, get_exchange_rates_for_days
from datetime import datetime, timedelta, date
from api.constants import *

sales_cache = {}
sales_cache_usd = {}

def update_cache_data():
    global sales_cache, sales_cache_usd
    sales_data = get_transaction_sums_for_days(YEARS)
    sorted_data = sorted(sales_data, key = lambda el: datetime.strptime(el[1], DB_DATE_FORMAT))
    dates = []
    rates = []
    sales = []
    sales_in_pln = []
    interpolated = []
    for s in sorted_data:
        sales.append(round(s[0], 4))
        dates.append(datetime.strptime(s[1], DB_DATE_FORMAT).strftime(DATE_FORMAT))
    rates = get_exchange_rates_for_days(dates)
    for i in range(len(sales)):
        sales_in_pln.append(round((sales[i] * rates[i][0]), 4))
        interpolated.append(rates[i][1])
    
    sales_dict = {}
    sales_dict_usd={}
    for i in range(len(dates)):
        sales_dict[dates[i]] = [sales_in_pln[i], interpolated[i]]
        sales_dict_usd[dates[i]] = [sales[i], interpolated[i]]
    sales_cache, sales_cache_usd = sales_dict, sales_dict_usd
    print("Cache update completed.")
    