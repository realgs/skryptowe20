from datetime import timedelta

from sales_database import SalesDatabaseManager
from sales_database import API_BASE_CURRENCY

SERVER = 'DESKTOP-LKE4F79'
DATABASE_NAME = 'AdventureWorks2019'

MIN_AVAILABLE_YEAR = 2011
MIN_AVAILABLE_MONTH = 5
MIN_AVAILABLE_DAY = 31


def get_sales_for_date_and_currency(currency, date_from, date_to):
    database_manager = SalesDatabaseManager(SERVER, DATABASE_NAME)
    update_currency_sales(database_manager, API_BASE_CURRENCY, date_from, date_to)
    if currency != API_BASE_CURRENCY:
        update_currency_sales(database_manager, currency, date_from, date_to)

    currency_sales = database_manager.get_total_sales_in_currency(currency, date_from, date_to)
    return currency_sales


def update_currency_sales(db_manager, currency, date_from, date_to):
    currency_sales = db_manager.get_total_sales_in_currency(currency, date_from, date_to)
    if len(currency_sales) == 0:
        db_manager.insert_currency_sales_data_to_table(currency, date_from, date_to)
    else:
        delta = date_to - date_from
        if len(currency_sales) < delta.days + 1:
            upload_missing_rows_to_database(db_manager, currency, date_from, date_to)


def upload_missing_rows_to_database(db_manager, currency, date_from, date_to):
    sale_date = date_from
    last_date = date_from
    empty_data_begin_date = date_from
    empty_data = False
    while sale_date <= date_to:
        date_exist_in_database = db_manager.get_currency_sale_for_date(currency, sale_date) is not None
        if not date_exist_in_database and not empty_data:
            empty_data_begin_date = sale_date
            empty_data = True
        elif date_exist_in_database and empty_data:
            db_manager.insert_currency_sales_data_to_table(currency, empty_data_begin_date, last_date)
            empty_data = False

        last_date = sale_date
        sale_date += timedelta(days=1)

    if empty_data:
        db_manager.insert_currency_sales_data_to_table(currency, empty_data_begin_date, last_date)
