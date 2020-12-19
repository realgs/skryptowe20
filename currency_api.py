from datetime import timedelta

from database import DatabaseManager

SERVER = 'DESKTOP-LKE4F79'
DATABASE_NAME = 'AdventureWorks2019'


def get_currency_rates(currency, date_from, date_to):
    database_manager = DatabaseManager(SERVER, DATABASE_NAME)
    db_rates = database_manager.get_currency_rates(currency, date_from, date_to)
    if len(db_rates) == 0:
        database_manager.insert_currency_data_to_table(currency, date_from, date_to)
        db_rates = database_manager.get_currency_rates(currency, date_from, date_to)
    else:
        delta = date_to - date_from
        if len(db_rates) < delta.days + 1:
            upload_missing_rows_to_database(database_manager, currency, date_from, date_to)
            db_rates = database_manager.get_currency_rates(currency, date_from, date_to)

    for row in db_rates:
        print(row)
    # CREATE AND THEN RETURN JSON


def upload_missing_rows_to_database(database, currency, date_from, date_to):
    currency_date = date_from
    last_date = date_from
    empty_data_begin_date = date_from
    empty_data = False
    while currency_date <= date_to:
        date_exist_in_database = database.get_currency_rate_for_date(currency, currency_date) is not None
        if not date_exist_in_database and not empty_data:
            empty_data_begin_date = currency_date
            empty_data = True
        elif date_exist_in_database and empty_data:
            database.insert_currency_data_to_table(currency, empty_data_begin_date, last_date)
            empty_data = False

        last_date = currency_date
        currency_date += timedelta(days=1)

    if empty_data:
        database.insert_currency_data_to_table(currency, empty_data_begin_date, last_date)
