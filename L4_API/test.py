import unittest
from .api_handler import currency_rates_and_dates, get_table


class TestSortingMethods(unittest.TestCase):

    def test_table_getter(self):
        table = get_table('USD')
        self.assertEqual(table, 'A')

        table = get_table('JOD')
        self.assertEqual(table, 'B')

        table = get_table('sdgdf')
        self.assertEqual(table, '')

        table = get_table('')
        self.assertEqual(table, '')

    def test_currency_rates(self):
        rates, _ = currency_rates_and_dates('USD', 1)
        self.assertEqual(rates, [3.7677])

        rates, _ = currency_rates_and_dates('JOD', 7)
        self.assertEqual(len(rates), 7)

        rates, dates = currency_rates_and_dates('USD', 7)
        self.assertEqual(len(rates), len(dates))

        rates, dates = currency_rates_and_dates('USD', 400)
        self.assertLess(len(rates), 366)

    def test_currency_rates_invalid_values(self):
        rates, _ = currency_rates_and_dates('USD', 0)
        self.assertEqual(rates, [])

        rates, _ = currency_rates_and_dates('USD', -1)
        self.assertEqual(rates, [])

        rates, _ = currency_rates_and_dates('dgdd', 1)
        self.assertEqual(rates, [])

        rates, _ = currency_rates_and_dates('', 1)
        self.assertEqual(rates, [])


if __name__ == '__main__':
    unittest.main()
