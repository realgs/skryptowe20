from datetime import date, timedelta
from datetime import datetime
import pyodbc

from currency_api_connector import CurrencyDataDownloader


class DatabaseManager:

    def __init__(self, server, database, table, currency):
        self.__conn = pyodbc.connect(
            "Driver={SQL Server Native Client 11.0};"
            f"Server={server};"
            f"Database={database};"
            "Trusted_Connection=yes;"
        )
        self.__cursor = self.__conn.cursor()
        self.__new_table_name = table
        self.__currency = currency

    def read(self):
        self.__cursor.execute(f"select * from {self.__new_table_name}")
        for row in self.__cursor:
            print(row)

    def create_table_with_currency_rates(self):
        self.__cursor.execute(f'''
          CREATE TABLE {self.__new_table_name} (
                QuotationDate DATETIME PRIMARY KEY,
                CurrencyRate REAL NOT NULL
          );
        ''')
        self.__conn.commit()

    def __get_price_for_date(self, currency_data, rate_date):
        pass

    def insert_currency_data_to_table(self):
        date_from = date(year=2011, month=1, day=1)
        delta = date.today() - date_from
        how_many_days = delta.days
        currency_data = CurrencyDataDownloader(). \
            get_currency_prices_for_last_days(self.__currency, how_many_days)

        if currency_data[0] is not None and len(currency_data[0]) > 0:
            oldest_date = datetime.strptime(currency_data[0][0][0], '%Y-%m-%d')
            dates = []
            rate_date = oldest_date
            while rate_date.date() < date.today() - timedelta(days=1):
                dates.append(rate_date)
                rate_date = rate_date + timedelta(days=1)

            currency_rates = []

            last_date = datetime.strptime(currency_data[0][0][0], '%Y-%m-%d')
            for data in currency_data[0]:
                rate_date = datetime.strptime(data[0], '%Y-%m-%d')
                delta = rate_date - last_date

                last_rate = data[1]
                last_date = rate_date
                if delta.days > 1:
                    for days_diff in range(delta.days):
                        currency_rates.append(last_rate)
                else:
                    currency_rates.append(data[1])

            for i in range(len(dates)):
                self.__cursor.execute(f'''
                    INSERT INTO {self.__new_table_name} (QuotationDate, CurrencyRate)
                    VALUES (?,?)''',
                                      dates[i], currency_rates[i])
            self.__conn.commit()

    def delete_table(self):
        self.__cursor.execute(f"DROP TABLE {self.__new_table_name};")
        self.__conn.commit()
