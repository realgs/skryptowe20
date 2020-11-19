import unittest
import requests
from .rates import currency_rates_dates


class TestSortingMethods(unittest.TestCase):

    def test_currency_rates(self):
        rates, _ = currency_rates_dates('USD', 1)
        self.assertEqual(rates, [3.9069])

        rates, _ = currency_rates_dates('JOD', 1)
        self.assertEqual(rates, [])

        rates, _ = currency_rates_dates('JOD', 7)
        self.assertEqual(rates, [5.5376])

    def test_currency_rates_invalid_values(self):
        rates, _ = currency_rates_dates('USD', 0)
        self.assertEqual(rates, [])

        rates, _ = currency_rates_dates('USD', -1)
        self.assertEqual(rates, [])

        rates, _ = currency_rates_dates('dgdd', 1)
        self.assertEqual(rates, [])

        rates, _ = currency_rates_dates('', 1)
        self.assertEqual(rates, [])


if __name__ == '__main__':
    unittest.main()
