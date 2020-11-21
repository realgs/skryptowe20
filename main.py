from chart_drawer import draw_currencies_chart
from currency_api_connector import CurrencyDataDownloader
from database_connector import DatabaseManager

if __name__ == '__main__':
    downloader = CurrencyDataDownloader()
    usd_data = downloader.get_currency_prices_for_last_days('usd', 180)
    eur_data = downloader.get_currency_prices_for_last_days('eur', 180)
    currencies_chart_data = [usd_data, eur_data]
    draw_currencies_chart(currencies_chart_data)

    server_name = 'DESKTOP-LKE4F79'
    database_name = 'AdventureWorks2019'
    table_name = 'CurrencyRatesForLastYears'
    connector = DatabaseManager(server_name, database_name, table_name, 'USD')
    connector.read()
