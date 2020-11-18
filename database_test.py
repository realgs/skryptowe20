import unittest
from currency_rates import get_rete_of_currency
from modify_database import _append_missing_dates, _DATE_FORMAT
from datetime import datetime, timedelta


class TestModifyDatabase(unittest.TestCase):

    def test_append_missing_dates(self):
        usd = get_rete_of_currency('usd', 365)
        rates = _append_missing_dates(usd['rates'])

        for i in range(len(rates) - 1):
            curr = datetime.strptime(rates[i]['effectiveDate'], _DATE_FORMAT)
            next = datetime.strptime(
                rates[i + 1]['effectiveDate'], _DATE_FORMAT)
            delta = next - curr
            self.assertEqual(1, delta.days)
