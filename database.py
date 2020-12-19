from datetime import timedelta
from datetime import datetime
import pyodbc

from currency_api_connector import CurrencyDataDownloader
import currencies


class DatabaseManager:

    def __init__(self, server, database):
        self.__min_available_year = 2002
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

    def create_currency_table(self, table_name):
        self.__cursor.execute(f'''
          CREATE TABLE {table_name} (
                QuotationDate DATETIME PRIMARY KEY,
                CurrencyRate REAL NOT NULL
          );
        ''')
        self.__conn.commit()

    def insert_currency_data_to_table(self, currency, date_from, date_to):
        if date_from > date_to:
            raise ValueError("date from must be before date to")

        table_name = self.__get_table_name_for_currency(currency)
        is_table_created = self.__check_currency_table_name_and_create(table_name)
        currency_data_downloader = CurrencyDataDownloader(currency)
        if is_table_created:
            currency_data = currency_data_downloader.get_currency_prices_for_dates(date_from, date_to)

            dates = []
            api_data_available_for_dates = currency_data[0] is not None and len(currency_data[0]) > 0
            if api_data_available_for_dates:
                oldest_date = datetime.strptime(currency_data[0][0][0], '%Y-%m-%d')
                rate_date = oldest_date
                while rate_date.date() <= date_to:
                    dates.append(rate_date)
                    rate_date += timedelta(days=1)
                currency_rates = self.__create_currency_rates_for_dates(currency_data)
                return self.__insert_currency_data(dates, currency_rates, table_name)
            else:
                last_available_rate = self.__get_first_available_rate_from_date(date_from, currency)
                rate_date = date_from
                currency_rates = []

                while rate_date <= date_to:
                    currency_rates.append(last_available_rate)
                    dates.append(rate_date)
                    rate_date += timedelta(days=1)

                return self.__insert_currency_data(dates, currency_rates, table_name)
        return None

    def __create_currency_rates_for_dates(self, currency_data):
        currency_rates = []
        last_date = datetime.strptime(currency_data[0][0][0], '%Y-%m-%d')
        last_rate = self.__get_first_available_rate_from_date(last_date, currency_data[1])

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
        return currency_rates

    def __get_first_available_rate_from_date(self, rate_date, currency):
        currency_data_downloader = CurrencyDataDownloader(currency)
        last_available_rate = 0
        last_available_rate_date = rate_date - timedelta(days=1)
        while last_available_rate == 0 and last_available_rate_date.year >= self.__min_available_year:
            rate_data = currency_data_downloader.\
                get_currency_prices_for_date(datetime.strftime(last_available_rate_date, '%Y-%m-%d'))
            if len(rate_data[0]) > 0 and rate_data[0][0] is not None:
                last_available_rate = rate_data[0][0][1]
            last_available_rate_date -= timedelta(days=1)

        return last_available_rate

    def __insert_currency_data(self, dates, currency_rates, table_name):
        if table_name is not None:
            for i in range(len(dates)):
                self.__cursor.execute(f'''
                    INSERT INTO {table_name} (QuotationDate, CurrencyRate)
                    VALUES (?,?)''',
                                      dates[i], currency_rates[i])
            self.__conn.commit()
            return True
        return False

    @staticmethod
    def __get_table_name_for_currency(currency):
        if currencies.AVAILABLE_CURRENCIES.__contains__(str(currency).upper()):
            return str(currency).upper() + '_Currency'
        else:
            return None

    def delete_table(self, table_name):
        self.__cursor.execute(f"DROP TABLE {table_name};")
        self.__conn.commit()

    def get_currency_rates(self, currency, date_from, date_to):
        table_name = self.__get_table_name_for_currency(currency)
        is_table_created = self.__check_currency_table_name_and_create(table_name)
        if is_table_created:
            self.__cursor.execute(
                f"SELECT QuotationDate, CurrencyRate FROM {table_name} WHERE QuotationDate "
                f"BETWEEN '{date_from}' AND '{date_to}' ORDER BY QuotationDate")
            rates = []
            for row in self.__cursor:
                rates.append(row)
            return rates
        return None

    def __check_currency_table_name_and_create(self, table_name):
        if table_name is not None:
            table_exist = self.__cursor.tables(table=table_name, tableType='TABLE').fetchone()
            if not table_exist:
                self.create_currency_table(table_name)
            return True
        return False

    def get_currency_rate_for_date(self, currency, date):
        table_name = self.__get_table_name_for_currency(currency)
        is_table_created = self.__check_currency_table_name_and_create(table_name)
        if is_table_created:
            self.__cursor.execute(
                f"SELECT QuotationDate, CurrencyRate FROM {table_name} "
                f"WHERE QuotationDate = '{date}' "
                f"ORDER BY QuotationDate")
            return self.__cursor.fetchone()
        return None
