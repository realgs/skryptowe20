import os
import requests
import sqlite3 as sql
from flask import jsonify
from datetime import datetime
from utilities_nbp import change_kwargs_to_two_days, to_date, OK_CODE, FROM, TILL, LAST
from utilities_database import TABLE_A, TABLE_B, DB_PATH, FIRST_DAY_OF_NBP_CURRENCY_RATE, TODAY

FIRST_EVER_SALES_DAY = "2006-10-01"
LAST_EVER_SALES_DAY = "2017-09-29"
NOT_ACCEPTABLE_CODE = 406


def universal_database_rates_call(code, inter, **kwargs):
    """
    Returns exchange rates from database or error message if given 
    arguments were invalid. And it returns error code.

    Args:
        code (str): code of currency 
        inter (bool): "interpolated" flag
        *kwargs: from_date (str) / till_date (str) /  last_days (str) 

    Returns:
        dict, int: exchange rates with days with/without "interpolated" flag, 
        error code
    """
    output, err_code = check_rates_request_data(code, kwargs)
    if err_code == OK_CODE:
        output = get_exchange_rates_from_database(code, inter, kwargs)
    else:
        output = {"Error": output}
    return output, err_code


def get_exchange_rates_from_database(code, interpolated, kwargs):
    """
    Returns exchange rated from database.

    Args:
        code (str): code of currency
        kwargs (dict): from_date (str) / till_date (str) /  last_days (str)

    Returns:
        dict: exchange rates with days and with/without "interpolated" flag
    """
    from_date, till_date = change_kwargs_to_two_days(kwargs, code)
    conn = sql.connect(DB_PATH)
    c = conn.cursor()
    select_cmd = f"""
    SELECT date, rate {'{}'} FROM {code}_exchange_rate_table
    WHERE '{from_date}' <= date AND date <= '{till_date}'
    """
    if interpolated:
        c.execute(select_cmd.format(", interpolated"))
        data = c.fetchall()
        output = [{"date": d, "rate": r, "interpolated": i} for d, r, i in data]
    else:
        c.execute(select_cmd.format(""))
        data = c.fetchall()
        output = [{"date": d, "rate": r} for d, r in data]
    conn.close()
    return jsonify(output)


def get_sales_from_database(code, from_date, till_date=None):
    """
    Returns sum of sales from given period in 2 currencies - original (USD) 
    and requested with code. Or error message with error code.

    Args:
        code (str): code of currency
        from_date (str): first day of period
        till_date (str): last day of period

    Retruns:
        dict, int: sales data from database, error code
    """
    if not till_date:
        till_date = from_date
    err_msg, err_code = check_sales_request_data(code, from_date, till_date)
    if err_code != OK_CODE:
        return {"Error": err_msg}, err_code
    elif code.lower() == "pln":
        return get_sales_in_pln(from_date, till_date), err_code
    else:
        return get_sales_in_foreign_curr(code, from_date, till_date), err_code


def get_sales_in_pln(from_date, till_date):
    """
    Returns sales data in original currency (USD) and in PLN.

    Args:
        from_date (str): first day of period
        till_date (str): last day of period

    Retruns:
        dict, int: sales data from database
    """
    conn = sql.connect(DB_PATH)
    c = conn.cursor()
    select_cmd = f"""
    SELECT USD.date, SUM(IFNULL(S.SaleAmount,0)), ROUND(SUM(IFNULL(S.SaleAmount,0)) 
    * USD.rate, 2), USD.rate 
    FROM usd_exchange_rate_table AS USD 
    LEFT JOIN SALES AS S ON USD.date=S.DateRecorded
    GROUP BY USD.date 
    HAVING '{from_date}' <= USD.date AND USD.date <= '{till_date}'
    """
    c.execute(select_cmd)
    data = c.fetchall()
    conn.close()
    output = [{"Date": d, "USD sales": v1, f"PLN sales": v2, "USD rate": v3}
              for d, v1, v2, v3 in data]
    return jsonify(output)


def get_sales_in_foreign_curr(code, from_date, till_date):
    """
    Returns sales data in original currency (USD) and foreign one given as code.

    Args:
        code (str): code of currency
        from_date (str): first day of period
        till_date (str): last day of period

    Retruns:
        dict, int: sales data from database
    """
    conn = sql.connect(DB_PATH)
    c = conn.cursor()
    select_cmd = f"""
    SELECT USD.date, SUM(IFNULL(S.SaleAmount,0)), ROUND(SUM(IFNULL(S.SaleAmount,0)) 
    * USD.rate / BUF.rate, 2), USD.rate , BUF.rate 
    FROM usd_exchange_rate_table AS USD 
    JOIN {code}_exchange_rate_table AS BUF ON USD.date = BUF.date 
    LEFT JOIN SALES AS S ON USD.date=S.DateRecorded
    GROUP BY USD.date 
    HAVING '{from_date}' <= USD.date AND USD.date <= '{till_date}'
    """
    c.execute(select_cmd)
    data = c.fetchall()
    conn.close()
    output = [{"Date": d, "USD sales": v1, f"{code.upper()} sales": v2, "USD rate": v3,
               f"{code.upper()} rate": v4} for d, v1, v2, v3, v4 in data]
    return jsonify(output)


def check_rates_request_data(code, kwargs):
    """
    Checks whether given arguments are valid. Code should be in TABLE_A or TABLE_B.
    Dates should be from between first ever and actual days of exchange rates, 
    and till_date cannot be past from_date. Argument last_days must be positive.

    Args:
        code (str): code of currency 
        kwargs (dict): from_date (str) / till_date (str) /  last_days (str)

    Returns:
        str: possible error message, int: error code
    """
    err_msg = ""
    err_code = OK_CODE
    min_date = to_date(FIRST_DAY_OF_NBP_CURRENCY_RATE)
    today_date = to_date(TODAY())
    
    # Code
    if code.lower() not in (TABLE_A + TABLE_B):
        err_msg = f"Given currency code is not available: {code}"

    # Last days
    if LAST in kwargs:
        date_limit = today_date - min_date
        if kwargs[LAST] <= 0:
            err_msg = f"Argument last_days must be positive: {kwargs[LAST]}"
        elif kwargs[LAST] > date_limit.days:
            err_msg = f"Min date limit reached: min {date_limit.days} days"

    if err_msg:
        return err_msg, NOT_ACCEPTABLE_CODE     
    
    # Dates format
    from_date = 0
    till_date = 0
    try:
        if FROM in kwargs:
            from_date = to_date(kwargs[FROM])
        if TILL in kwargs:  
            till_date = to_date(kwargs[TILL])
    except ValueError:
        err_msg = "Wrong date format"
        return err_msg, NOT_ACCEPTABLE_CODE
    
    # Date range
    if from_date and (from_date < min_date or today_date < from_date):
        err_msg = "Date over limit"
        return err_msg, NOT_ACCEPTABLE_CODE
    
    if till_date:
        if till_date < min_date or today_date < till_date:
            err_msg = "Date over limit"
            err_code = NOT_ACCEPTABLE_CODE
        elif from_date > till_date:
            err_msg = "From date cannot be past till date"
            err_code = NOT_ACCEPTABLE_CODE
    return err_msg, err_code

def check_sales_request_data(code, from_date, till_date):
    """
    Checks whether given arguments are valid. Code should not be in USD 
    (original currency), and dates should be from between first ever and 
    last ever days of sales data, and till_date cannot be past from_date.

    Args:
        code (str): code of currency 
        from_date (str): first day of period
        till_date (str): last day of period

    Returns:
        str: possible error message, int: err_code
    """
    err_msg = None
    if (code.lower() not in (TABLE_A + TABLE_B) and code.lower() != "pln") or code.lower() == "usd":
        err_msg = f"Given currency code is not available: {code}"
    elif from_date < FIRST_EVER_SALES_DAY:
        err_msg = f"This date is too early!: {from_date}. Min: {FIRST_EVER_SALES_DAY}"
    elif till_date > LAST_EVER_SALES_DAY:
        err_msg = f"This date is too late!: {till_date}. Max: {LAST_EVER_SALES_DAY}"
    elif till_date < from_date:
        err_msg = f"till_date must be after from_date!: {from_date} > {till_date}!"
    return err_msg, NOT_ACCEPTABLE_CODE if err_msg else OK_CODE
