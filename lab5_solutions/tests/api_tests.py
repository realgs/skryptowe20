import unittest
import requests

HOME_PATH = 'http://127.0.0.1:5000'
EXCHANGE_RATES_PART = '/exchange-rates/'
SALES_PART = '/sales/'

INVALID_DATE_FORMAT_MSG = 'Invalid date format:'
WRONG_CURRENCY_MSG = 'This currency is not supported:'
DATE_NOT_IN_RANGE_MSG = 'Date must be in range:'
START_DATE_AFTER_END_DATE_MSG = 'cannot be after the end date:'

CORRECT_DATE = '2015-11-13'
CORRECT_CURRENCY = 'EUR'


class TestCorrectnessOfRequest(unittest.TestCase):

    def setUp(self) -> None:

        self.correct_currencies = ['GBP',
                                   'EUR',
                                   'USD']

        self.wrong_currencies = ['ABC',
                                 'EFG',
                                 '123']

        self.correct_days = ['2015-01-02',
                             '2015-03-12',
                             '2015-12-18',
                             '2016-11-20',
                             '2016-11-30']

        self.wrong_days = ['2020-11-21',
                           '2019-11-11',
                           '2006-01-03',
                           '2010-12-24',
                           '2012-01-01']

        self.invalid_days = ['2015-11-40',
                             '2019-11-abc',
                             '2015-01']

        self.correct_periods = [['2014-12-28', '2014-12-31'],
                                ['2015-02-04', '2015-04-09'],
                                ['2015-07-09', '2016-01-13'],
                                ['2015-01-03', '2015-01-04'],
                                ['2016-11-10', '2016-11-10']]

        self.wrong_periods = [['2015-11-23', '2015-11-20'],
                              ['2015-11-14', '2015-11-11'],
                              ['2016-11-11', '2015-11-11']]

    def test_currencies_checker(self):
        for curr in self.correct_currencies:
            path = HOME_PATH + EXCHANGE_RATES_PART + curr + '/' + CORRECT_DATE
            response = requests.get(path)
            status_code = response.status_code
            self.assertEqual(200, status_code)

        for curr in self.wrong_currencies:
            path = HOME_PATH + EXCHANGE_RATES_PART + curr + '/' + CORRECT_DATE
            response = requests.get(path)
            status_code = response.status_code
            self.assertTrue(response.text.__contains__(WRONG_CURRENCY_MSG))
            self.assertEqual(400, status_code)

    def test_date_checker(self):
        for date in self.correct_days:
            path = HOME_PATH + EXCHANGE_RATES_PART + CORRECT_CURRENCY + '/' + date
            response = requests.get(path)
            status_code = response.status_code
            self.assertEqual(200, status_code)

        for date in self.wrong_days:
            path = HOME_PATH + EXCHANGE_RATES_PART + CORRECT_CURRENCY + '/' + date
            response = requests.get(path)
            status_code = response.status_code
            self.assertTrue(response.text.__contains__(DATE_NOT_IN_RANGE_MSG))
            self.assertEqual(400, status_code)

    def test_date_string_to_datetime_converter(self):
        for date in self.invalid_days:
            path = HOME_PATH + EXCHANGE_RATES_PART + CORRECT_CURRENCY + '/' + date
            response = requests.get(path)
            status_code = response.status_code
            self.assertTrue(response.text.__contains__(INVALID_DATE_FORMAT_MSG))
            self.assertEqual(400, status_code)

    def test_date_range_checker(self):
        for period in self.correct_periods:
            path = HOME_PATH + EXCHANGE_RATES_PART + CORRECT_CURRENCY + '/' + period[0] + '/' + period[1]
            response = requests.get(path)
            status_code = response.status_code
            self.assertEqual(200, status_code)

        for period in self.wrong_periods:
            path = HOME_PATH + EXCHANGE_RATES_PART + CORRECT_CURRENCY + '/' + period[0] + '/' + period[1]
            response = requests.get(path)
            status_code = response.status_code
            self.assertTrue(response.text.__contains__(START_DATE_AFTER_END_DATE_MSG))
            self.assertEqual(400, status_code)


class TestApi(unittest.TestCase):

    def setUp(self) -> None:
        self.zero_sale_date = '2015-02-12'

        self.zero_sale_json = {
            "sales": [
                {
                    "date": "2015-02-12",
                    "pln": 0,
                    "usd": 0
                }
            ]
        }

        self.exchange_rate_one_day_json = {
            "rates": [
                {
                    "currency": "EUR",
                    "date": "2015-11-13",
                    "interpolated": False,
                    "rate": 4.2362
                }
            ]
        }

        self.exchange_rate_date = ['2015-11-10', '2015-11-13']

        self.exchange_rate_period_json = {
            "rates": [
                {
                    "currency": "EUR",
                    "date": "2015-11-10",
                    "interpolated": False,
                    "rate": 4.2485
                },
                {
                    "currency": "EUR",
                    "date": "2015-11-11",
                    "interpolated": True,
                    "rate": 4.2485
                },
                {
                    "currency": "EUR",
                    "date": "2015-11-12",
                    "interpolated": False,
                    "rate": 4.2245
                },
                {
                    "currency": "EUR",
                    "date": "2015-11-13",
                    "interpolated": False,
                    "rate": 4.2362
                }
            ]
        }

        self.sale_one_day_json = {
            "sales": [
                {
                    "date": "2015-11-13",
                    "pln": 4244.32,
                    "usd": 708.0
                }
            ]
        }

        self.sale_date = ['2015-11-10', '2015-11-13']

        self.sale_period_json = {
            "sales": [
                {
                    "date": "2015-11-10",
                    "pln": 6996.13,
                    "usd": 1170.0
                },
                {
                    "date": "2015-11-11",
                    "pln": 2062.96,
                    "usd": 345.0
                },
                {
                    "date": "2015-11-12",
                    "pln": 5102.12,
                    "usd": 852.0
                },
                {
                    "date": "2015-11-13",
                    "pln": 4244.32,
                    "usd": 708.0
                }
            ]
        }

    def test_zero_sale_date(self):
        path = HOME_PATH + SALES_PART + self.zero_sale_date
        response = requests.get(path)
        status_code = response.status_code
        self.assertEqual(response.json(), self.zero_sale_json)
        self.assertEqual(200, status_code)

    def test_rate_one_day(self):
        path = HOME_PATH + EXCHANGE_RATES_PART + CORRECT_CURRENCY + '/' + CORRECT_DATE
        response = requests.get(path)
        status_code = response.status_code
        self.assertEqual(response.json(), self.exchange_rate_one_day_json)
        self.assertEqual(200, status_code)

    def test_rate_from_date_to_date(self):
        path = HOME_PATH + EXCHANGE_RATES_PART + CORRECT_CURRENCY + '/' + self.exchange_rate_date[0] + '/' + \
               self.exchange_rate_date[1]
        response = requests.get(path)
        status_code = response.status_code
        self.assertEqual(response.json(), self.exchange_rate_period_json)
        self.assertEqual(200, status_code)

    def test_sale_one_day(self):
        path = HOME_PATH + SALES_PART + CORRECT_DATE
        response = requests.get(path)
        status_code = response.status_code
        self.assertEqual(response.json(), self.sale_one_day_json)
        self.assertEqual(200, status_code)

    def test_sale_from_date_to_date(self):
        path = HOME_PATH + SALES_PART + self.sale_date[0] + '/' + \
               self.sale_date[1]
        response = requests.get(path)
        status_code = response.status_code
        self.assertEqual(response.json(), self.sale_period_json)
        self.assertEqual(200, status_code)
