import unittest
from .rates import currency_rates_dates, _get_table


class TestSortingMethods(unittest.TestCase):

    def test_table_getter(self):
        table = _get_table('USD')
        self.assertEqual(table, 'A')

        table = _get_table('JOD')
        self.assertEqual(table, 'B')

        table = _get_table('sdgdf')
        self.assertEqual(table, '')

        table = _get_table('')
        self.assertEqual(table, '')

    def test_currency_rates(self):
        rates, _ = currency_rates_dates('USD', 1)
        self.assertEqual(rates, [3.7872])

        rates, _ = currency_rates_dates('JOD', 1)
        self.assertEqual(rates, [])

        rates, _ = currency_rates_dates('JOD', 7)
        self.assertEqual(len(rates), 1)

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
