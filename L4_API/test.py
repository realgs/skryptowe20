import unittest
import requests
from .rates import currency_rates


class TestSortingMethods(unittest.TestCase):

    def test_currency_rates(self):
        rates, _ = currency_rates('USD', 1)
        self.assertEqual(rates, [3.9069])

        rates, _ = currency_rates('JOD', 1)
        self.assertEqual(rates, [])

        rates, _ = currency_rates('JOD', 7)
        self.assertEqual(rates, [5.5376])

    def test_currency_rates_invalid_values(self):
        rates, _ = currency_rates('USD', 0)
        self.assertEqual(rates, [])

        rates, _ = currency_rates('USD', -1)
        self.assertEqual(rates, [])

        rates, _ = currency_rates('dgdd', 1)
        self.assertEqual(rates, [])

        rates, _ = currency_rates('', 1)
        self.assertEqual(rates, [])


if __name__ == '__main__':
    unittest.main()
