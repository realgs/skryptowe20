import unittest
from datetime import date
from decimal import Decimal
from lab4.app.src.app import mix_dollar_euro_rates, calculate_daily_orders


class MixRatesReceiverTests(unittest.TestCase):
    def test_mix_dollar_euro_rates(self):
        dollar_response = ({'rates': [
            {"date": '2020-01-01', "rate": 3.90},
            {"date": '2020-01-02', "rate": 3.86},
            {"date": '2020-01-03', "rate": 3.92}
        ]}, 200)
        euro_response = ({'rates': [
            {"date": '2020-01-01', "rate": 4.21},
            {"date": '2020-01-02', "rate": 4.23},
            {"date": '2020-01-03', "rate": 4.22}
        ]}, 200)

        expected_result = ({'rates': [
            {"date": '2020-01-01', "dollarRate": 3.90, "euroRate": 4.21},
            {"date": '2020-01-02', "dollarRate": 3.86, "euroRate": 4.23},
            {"date": '2020-01-03', "dollarRate": 3.92, "euroRate": 4.22}
        ]}, 200)

        result = mix_dollar_euro_rates(dollar_response, euro_response)
        self.assertEqual(expected_result, result)

    def test_mix_empty_dollar_euro_rates(self):
        dollar_response = ({'rates': []}, 200)
        euro_response = ({'rates': []}, 200)
        expected_result = ({'rates': []}, 200)
        result = mix_dollar_euro_rates(dollar_response, euro_response)
        self.assertEqual(expected_result, result)

    def test_empty_dollar_euro_rates_failure(self):
        dollar_response = ({'rates': [{"date": '2020-01-01', "rate": 3.90}]}, 200)
        euro_response = ({'error': 'There was an error'}, 400)
        expected_result = ({'error': 'There was an error'}, 400)
        result = mix_dollar_euro_rates(dollar_response, euro_response)
        self.assertEqual(expected_result, result)


class CalculateDailyOrders(unittest.TestCase):
    def test_calculate_daily_orders(self):
        usd_rates = [
            {'date': date(2019, 1, 1), 'plnRate': Decimal('3.7619')},
            {'date': date(2019, 1, 2), 'plnRate': Decimal('3.7619')},
            {'date': date(2019, 1, 3), 'plnRate': Decimal('3.7827')}
        ]
        orders = [
            {'id': 305, 'date': date(2019, 1, 1), 'totalAmount': Decimal('430.03')},
            {'id': 131, 'date': date(2019, 1, 1), 'totalAmount': Decimal('88.42')},
            {'id': 770, 'date': date(2019, 1, 1), 'totalAmount': Decimal('58.81')},
            {'id': 94, 'date': date(2019, 1, 2), 'totalAmount': Decimal('245.99')},
            {'id': 28, 'date': date(2019, 1, 2), 'totalAmount': Decimal('198.19')},
            {'id': 107, 'date': date(2019, 1, 2), 'totalAmount': Decimal('154.22')},
            {'id': 101, 'date': date(2019, 1, 2), 'totalAmount': Decimal('142.61')},
            {'id': 582, 'date': date(2019, 1, 2), 'totalAmount': Decimal('308.50')},
            {'id': 191, 'date': date(2019, 1, 3), 'totalAmount': Decimal('314.91')},
            {'id': 15, 'date': date(2019, 1, 3), 'totalAmount': Decimal('96.85')},
            {'id': 187, 'date': date(2019, 1, 3), 'totalAmount': Decimal('352.00')},
            {'id': 59, 'date': date(2019, 1, 3), 'totalAmount': Decimal('340.32')},
            {'id': 780, 'date': date(2019, 1, 3), 'totalAmount': Decimal('415.90')}
        ]
        expected_daily_orders = [
            {'date': '2019-01-01', 'totalAmountPln': 2171.59, 'totalAmountUsd': 577.26},
            {'date': '2019-01-02', 'totalAmountPln': 3948.15, 'totalAmountUsd': 1049.51},
            {'date': '2019-01-03', 'totalAmountPln': 5749.63, 'totalAmountUsd': 1519.98}
        ]
        daily_orders = calculate_daily_orders(usd_rates, orders)
        self.assertEqual(expected_daily_orders, daily_orders)

    def test_empty_calculate_daily_orders(self):
        usd_rates = []
        orders = []
        expected_daily_orders = []
        daily_orders = calculate_daily_orders(usd_rates, orders)
        self.assertEqual(expected_daily_orders, daily_orders)
