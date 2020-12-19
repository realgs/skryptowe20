from database_connector import DatabaseManager
from datetime import datetime


def parse_str_to_date(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d').date()


if __name__ == '__main__':
    str_date_from = "2020-11-10"
    str_date_to = "2020-11-13"

    date_from = parse_str_to_date(str_date_from)
    date_to = parse_str_to_date(str_date_to)

    server_name = 'DESKTOP-LKE4F79'
    database_name = 'AdventureWorks2019'
    table_name = 'CurrencyRatesForLastYears'
    db_manager = DatabaseManager(server_name, database_name)
    db_manager.delete_table(table_name)
    db_manager.create_table_with_currency_rates(table_name)
    db_manager.insert_currency_data_to_table(table_name, 'USD')
    db_manager.read(table_name, date_from, date_to)
