from datetime import date, timedelta
from datetime import datetime
import pyodbc

from currency_api_connector import CurrencyDataDownloader


class DatabaseManager:

    def __init__(self, server, database):
        self.__conn = pyodbc.connect(
            "Driver={SQL Server Native Client 11.0};"
            f"Server={server};"
            f"Database={database};"
            "Trusted_Connection=yes;"
        )
        self.__cursor = self.__conn.cursor()

    def read(self, table_name, date_from, date_to):
        self.__cursor.execute(f"select * from {table_name}"
                              f" where QuotationDate between '{date_from}' AND '{date_to}'")
        for row in self.__cursor:
            print(row)

    def create_table_with_currency_rates(self, table_name):
        self.__cursor.execute(f'''
          CREATE TABLE {table_name} (
                QuotationDate DATETIME PRIMARY KEY,
                CurrencyRate REAL NOT NULL
          );
        ''')
        self.__conn.commit()

    def insert_currency_data_to_table(self, table_name, currency):
        date_from = date(year=2011, month=1, day=1)
        delta = date.today() - date_from
        how_many_days = delta.days
        currency_data = CurrencyDataDownloader(currency). \
            get_currency_prices_for_last_days(how_many_days)

        if currency_data[0] is not None and len(currency_data[0]) > 0:
            oldest_date = datetime.strptime(currency_data[0][0][0], '%Y-%m-%d')
            dates = []
            rate_date = oldest_date
            while rate_date.date() < date.today() - timedelta(days=1):
                dates.append(rate_date)
                rate_date = rate_date + timedelta(days=1)

            currency_rates = []

            last_rate = 0
            last_date = datetime.strptime(currency_data[0][0][0], '%Y-%m-%d')

            for data in currency_data[0]:
                rate_date = datetime.strptime(data[0], '%Y-%m-%d')
                delta = rate_date - last_date

                if delta.days > 1:
                    for days_diff in range(delta.days - 1):
                        currency_rates.append(last_rate)
                    currency_rates.append(data[1])
                else:
                    currency_rates.append(data[1])
                last_rate = data[1]
                last_date = rate_date

            for i in range(len(dates)):
                self.__cursor.execute(f'''
                    INSERT INTO {table_name} (QuotationDate, CurrencyRate)
                    VALUES (?,?)''',
                                      dates[i], currency_rates[i])
            self.__conn.commit()

    def delete_table(self, table_name):
        self.__cursor.execute(f"DROP TABLE {table_name};")
        self.__conn.commit()

    def get_total_sales(self, date_from, date_to):
        self.__cursor.execute(
            f"SELECT OrderDate, SUM(TotalDue) FROM Sales.SalesOrderHeader WHERE OrderDate "
            f"BETWEEN '{date_from}' AND '{date_to}' GROUP BY OrderDate ORDER BY OrderDate")

        total_sales = []
        for row in self.__cursor:
            total_sales.append(row)
        return total_sales

    def get_currency_rates(self, table_name, date_from, date_to):
        self.__cursor.execute(
            f"SELECT QuotationDate, CurrencyRate FROM {table_name} WHERE QuotationDate "
            f"BETWEEN \'{date_from}\' AND \'{date_to}\' ORDER BY QuotationDate")
        rates = []
        for row in self.__cursor:
            rates.append(row)
        return rates
