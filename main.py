from chart_drawer import draw_currencies_chart
from chart_drawer import draw_total_sales_chart
from currency_api_connector import CurrencyDataDownloader
from database_connector import DatabaseManager
from datetime import datetime


def parse_str_to_date(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d').date()


if __name__ == '__main__':
    str_date_from = "2011-10-01"
    str_date_to = "2012-10-10"
    date_from = parse_str_to_date(str_date_from)
    date_to = parse_str_to_date(str_date_to)
    downloader = CurrencyDataDownloader()

    usd_data = downloader.get_currency_prices_for_dates('usd', date_from, date_to)
    eur_data = downloader.get_currency_prices_for_dates('eur', date_from, date_to)
    currencies_chart_data = [usd_data, eur_data]
    draw_currencies_chart(currencies_chart_data)

    server_name = 'DESKTOP-LKE4F79'
    database_name = 'AdventureWorks2019'
    table_name = 'CurrencyRatesForLastYears'
    db_manager = DatabaseManager(server_name, database_name, table_name, 'USD')
    draw_total_sales_chart(db_manager, str_date_from, str_date_to)
