from unittest import TestCase

from rates import get_date_ranges, MAX_DAYS


class TestGetAvgRates(TestCase):
    def test_range_for_one_day(self):
        days_num = 1
        dates = get_date_ranges(days_num)

        # One day should only have one range
        self.assertEqual(len(dates), 1)

        # The dates should be equal for one day
        self.assertEqual(dates[0][0], dates[0][1])

    def test_one_range_for_value_smaller_than_limit(self):
        days_num = MAX_DAYS
        dates = get_date_ranges(days_num)

        # Only one range
        self.assertEqual(len(dates), 1)

        # The whole range should cover days_num - 1 days
        delta = dates[0][1] - dates[0][0]
        self.assertEqual(delta.days, days_num - 1)

    def test_two_ranges_for_value_bigger_than_limit(self):
        days_num = MAX_DAYS + 1
        dates = get_date_ranges(days_num)

        # Two ranges for MAX_DAYS + 1
        self.assertEqual(len(dates), 2)

        # The whole range should cover days_num - 1 days
        delta = dates[1][1] - dates[0][0]
        self.assertEqual(delta.days, days_num - 1)

        # First range should be only one day
        self.assertEqual(dates[0][0], dates[0][1])

    def test_date_diff_between_ranges(self):
        days_num = MAX_DAYS * 4
        dates = get_date_ranges(days_num)

        # The whole range should cover days_num - 1 days
        delta = dates[len(dates) - 1][1] - dates[0][0]
        self.assertEqual(delta.days, days_num - 1)

        # Difference between next ranges should be one day
        for older, newer in zip(dates[:-1], dates[1:]):
            diff = newer[0] - older[1]
            self.assertEqual(diff.days, 1)

    def test_illegal_number_of_days(self):
        days_num = 0
        with self.assertRaises(ValueError):
            get_date_ranges(days_num)
