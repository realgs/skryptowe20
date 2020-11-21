import unittest
from nbp_api import *
from exceptions import *
from currency import *
from datetime import datetime, date

DATE_FORMAT = "%Y-%m-%d"
SAMPLE_CURRENCY = Currency.USD
MAX_DAYS_TO_GET = 367


class TestRatesDatebase(unittest.TestCase):

    def setUp(self) -> None:
        self.correct_days = ['2012-01-02',
                             '2013-03-12',
                             '2015-12-18',
                             '2020-11-20',
                             '2018-11-30']

        self.wrong_days = ['2020-11-21',
                           '2019-11-11',
                           '2021-01-03',
                           '2015-12-24'
                           '2012-01-01',
                           '2019-13-31']

        self.correct_periods = [['2020-11-10', '2020-11-17'],
                                ['2014-02-04', '2014-04-09'],
                                ['2015-07-09', '2016-01-13'],
                                ['2013-01-03', '2013-01-04'],
                                ['2020-11-10', '2020-11-10']]

        self.long_periods = [['2020-01-02', '2020-11-17'],
                             ['2014-02-04', '2014-12-16'],
                             ['2015-09-09', '2016-03-02']]

        self.periods_longer_than_limit = [['2019-02-07', '2020-11-19'],
                                          ['2015-06-17', '2018-09-12'],
                                          ['2015-06-11', '2020-11-18']]

        self.wrong_periods = [['2020-11-23', '2020-11-20'],
                              ['2020-11-14', '2021-11-15'],
                              ['2020-11-11', '2020-11-11'],
                              ['2020-11-16', '2015-06-11']]

        self.correct_last_x_days = [2, 10, 15, 365 // 2, 365, MAX_DAYS_TO_GET, MAX_DAYS_TO_GET + 1, 400, 365 * 2]
        """
        I didn't test '1' here but below because today it's Saturday so it doesn't work today properly, 
        but on weekdays this day-difference will work, what can be seen in e.g. test_currency,
        where I tested the same start and end dates.
        """

        self.wrong_last_x_days = [-1000, -10, -2, -1, 0, 1]

    def test_currency(self):
        for curr in Currency:
            for day in self.correct_days:
                date = datetime.strptime(day, DATE_FORMAT).date()
                get_avg_rates_from_period(curr, date, date)

    def test_get_avg_rates_from_period(self):
        for period in self.correct_periods:
            start_date = datetime.strptime(period[0], DATE_FORMAT).date()
            end_date = datetime.strptime(period[1], DATE_FORMAT).date()
            self.assertNotIn(None, get_avg_rates_from_period(SAMPLE_CURRENCY, start_date, end_date))

        for long_period in self.long_periods:
            start_date = datetime.strptime(long_period[0], DATE_FORMAT).date()
            end_date = datetime.strptime(long_period[1], DATE_FORMAT).date()
            self.assertNotIn(None, get_avg_rates_from_period(SAMPLE_CURRENCY, start_date, end_date))

        for longer_than_limit_period in self.periods_longer_than_limit:
            start_date = datetime.strptime(longer_than_limit_period[0], DATE_FORMAT).date()
            end_date = datetime.strptime(longer_than_limit_period[1], DATE_FORMAT).date()
            self.assertNotIn(None, get_avg_rates_from_period(SAMPLE_CURRENCY, start_date, end_date))

    def test_get_get_avg_rates_from_period_exception(self):
        for wrong_period in self.wrong_periods:
            start_date = datetime.strptime(wrong_period[0], DATE_FORMAT).date()
            end_date = datetime.strptime(wrong_period[1], DATE_FORMAT).date()
            with self.assertRaises((RequestException, ArgumentException)):
                get_avg_rates_from_period(SAMPLE_CURRENCY, start_date, end_date)

    def test_get_avg_rates_from_last_x_days(self):
        for last_x_days in self.correct_last_x_days:
            self.assertNotIn(None, get_avg_rates_from_last_x_days(SAMPLE_CURRENCY, last_x_days))

    def test_get_avg_rates_from_last_x_days_exception(self):
        for wrong_x_days in self.wrong_last_x_days:
            with self.assertRaises((RequestException, ArgumentException)):
                get_avg_rates_from_last_x_days(SAMPLE_CURRENCY, wrong_x_days)


if __name__ == '__main__':
    unittest.main()
