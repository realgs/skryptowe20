import os
import requests
import pandas as pd
import sqlite3 as sql
from datetime import datetime, timedelta


FROM = "from_date"
TILL = "till_date"
LAST = "last_days"
ERROR = "Error"
LAST_DAYS_TO_CHECK = 14
API_URL = "http://api.nbp.pl/api/exchangerates/rates/{}/{}/{}/{}/"
DEFAULT_ERR_MSG = "Cannot figure out these arguments: {} {} {} {}"
OK_CODE = 200
NOT_FOUND_CODE = 404


def call_nbp_api_for(code, table, **kwargs):
    """
    Returns dict with daily exchange rates of given currency.
    Data is taken from NBP Api and then fixed.

    Args:
        code (str): code of currency
        table (str): name of table
        *kwargs: from_date (str) / till_date (str) /  last_days (str) 

    Returns:
        dict: sorted exchange rates with dates and "iterpolated" flags
    """
    # Parse args to readable form of two days
    from_date, till_date = change_kwargs_to_two_days(kwargs, code, table)

    # Split given period to smaller ones
    dt_till = datetime.combine(till_date, datetime.min.time())
    dt_from = datetime.combine(from_date, datetime.min.time())
    if (dt_till-dt_from).days > 365:
        return split_api_calls(from_date, till_date, code, table)

    # Get data from NBP Api
    till_date = str(till_date)
    from_date = str(from_date)
    link = API_URL.format(table, code, from_date, till_date)
    nbp_req = requests.get(link)
    
    # Parse NBP data into python dicts
    if nbp_req.status_code == OK_CODE:
        result = nbp_api_call_was_successful(nbp_req)
    elif nbp_req.status_code == NOT_FOUND_CODE and till_date == from_date and "repeating" not in kwargs:
        return nbp_api_call_error_while_reapeating(from_date, till_date, code, table)
    elif "repeating" not in kwargs:
        raise ValueError(DEFAULT_ERR_MSG.format(
            code, table, from_date, till_date))
    else:
        return

    return repair_exchange_data(result, from_date, till_date, code, table)


def nbp_api_call_was_successful(nbp_req):
    """
    Parses json returned from NBP Api into useful dict.

    Args:
        nbp_req (Response): response from NBP Api 

    Returns:
        dict: exchange rates with days and "iterpolated" flags
    """
    result = {}
    for buf in nbp_req.json()["rates"]:
        result[buf["effectiveDate"]] = [buf["mid"], 0]
    return result


def nbp_api_call_error_while_reapeating(from_date, till_date, code, table):
    """
    Returns first found result of exchange rate from past 14 days.

    Args:
        from_date (datetime.date): first day of period
        till_date (datetime.date): last days of period
        code (str): code of currency 
        table (str): name of table

    Returns:
        dict: day with exchange rate and "interpolated" flags
    """
    for i in range(LAST_DAYS_TO_CHECK):
        buf_day = to_date(till_date) - timedelta(days=i)
        buf_result = call_nbp_api_for(
            code, table, from_date=buf_day, till_date=buf_day, repeating=i)
        if isinstance(buf_result, dict):
            return {from_date:list(buf_result.values())[0]}
    raise ValueError(DEFAULT_ERR_MSG.format(
        code, table, from_date, till_date))


def change_kwargs_to_two_days(kwargs, code, table="ab"):
    """
    Parses strings from kwargs into two dates: from_date and till_date.

    Args:
        kwargs (dict): from_date (str) / till_date (str) / last_days (int)
        code (str): code of currency 
        table (str): name of table

    Returns:
        datetime.date, datetime.date: from date and till date
    """
    if LAST in kwargs:
        kwargs[TILL] = datetime.date(datetime.now())
        kwargs[FROM] = kwargs[TILL] - timedelta(kwargs[LAST] - 1)
    elif FROM in kwargs and TILL in kwargs:
        kwargs[TILL] = to_date(kwargs[TILL])
        kwargs[FROM] = to_date(kwargs[FROM])
    elif FROM in kwargs:
        kwargs[TILL] = datetime.date(datetime.now())
        kwargs[FROM] = to_date(kwargs[FROM])
    else:
        raise ValueError(DEFAULT_ERR_MSG.format(code, table, kwargs))
    return kwargs[FROM], kwargs[TILL]


def split_api_calls(from_date, till_date, code, table):
    """
    Splits one big NBP Api request into smaller ones (max 365 days per request).

    Args:
        from_date (datetime.date): first day of period
        till_date (datetime.date): last days of period
        code (str): code of currency
        table (str): name of table

    Returns:
        dict: exchange rates with dates and "iterpolated" flag s
    """
    total_result = {}
    start_date = from_date
    while start_date < till_date:
        buf_date = start_date
        start_date += timedelta(days=365)
        start_date = min(start_date, till_date)
        buf_res = call_nbp_api_for(code, table, from_date=buf_date, till_date=start_date)
        total_result.update(buf_res)
    return total_result


def repair_exchange_data(nbp_data, first_day, last_day, code, table):
    """
    Fixes missing exchange rates from NBP Api.

    Args:
        nbp_data (dict): data from NBP Api
        first_day (): first day of period
        last_day (): last day of period
        code (str): code of currency
        table (str): name of table

    Returns:
        dict: exchange rates with dates and "iterpolated" flags
    """
    # Check if the func was called for single-day period
    new_data = nbp_data.copy()
    if first_day == last_day:
        return new_data

    # Put missing days with None value into new_data
    buf_day = to_date(first_day)
    while buf_day <= to_date(last_day):
        str_buf_day = str(buf_day)
        if str_buf_day not in new_data:
            new_data[str_buf_day] = [None, 1]
        buf_day += timedelta(days=1)

    # Add rates to days that are in between other dates with exchange rates
    # or on the end of period
    for key, (val, _) in new_data.items():
        if not val:
            previous_day = str(to_date(key) - timedelta(days=1))
            if previous_day in new_data.keys():
                new_data[key][0] = new_data[previous_day][0]

    # Add missing rates from beginnig of period
    new_data = dict(sorted(new_data.items()))
    if None in [x[0] for x in new_data.values()]:
        buf_result = call_nbp_api_for(
            code, table, from_date=first_day, till_date=first_day)
        missing_rate = list(buf_result.values())[0][0]
        for key, (val, _) in new_data.items():
            if not val:
                new_data[key][0] = missing_rate
            else:
                break

    return new_data


def to_date(date):
    """
    Parses given str to datetime.date.

    Args:
        date (str): date to parse

    Returns:
        datetime.date: parsed date
    """
    return datetime.strptime(str(date), '%Y-%m-%d').date()
