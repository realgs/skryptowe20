import unittest
from currency_rates import get_rete_of_currency, _get_date_ranges


class TextGetRateOfCurrency(unittest.TestCase):

    def test_get_date_ranges(self):
        date_ranges = _get_date_ranges(400)
        self.assertEqual(2, len(date_ranges))
        self.assertNotEqual(date_ranges[0][1], date_ranges[1][0])

    def test_correct_params(self):
        get_rete_of_currency('usd', 365 // 2)

    def test_long_date_range(self):
        get_rete_of_currency('usd', 365 * 2)

    def test_wrong_type_params(self):
        self.assertRaises(TypeError, get_rete_of_currency, 'eur', 'dwa')
        self.assertRaises(TypeError, get_rete_of_currency, 'eur', 2.6)
        self.assertRaises(TypeError, get_rete_of_currency, 'eur', 2 + 4j)

        self.assertRaises(TypeError, get_rete_of_currency, 2, 2)
        self.assertRaises(TypeError, get_rete_of_currency, 2 + 4j, 2)
        self.assertRaises(TypeError, get_rete_of_currency, 2.6, 2)

    def test_wrong_delta(self):
        self.assertRaises(ValueError, get_rete_of_currency, 'eur', 0)
        self.assertRaises(ValueError, get_rete_of_currency, 'eur', -1)

    def test_no_such_currency(self):
        self.assertEqual([], get_rete_of_currency('euo', 2))
        self.assertEqual([], get_rete_of_currency('', 2))
