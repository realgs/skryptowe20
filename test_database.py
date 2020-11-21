import unittest
from database import add_missing_dates

class TestDatabase(unittest.TestCase):
  def test_add_missing_dates(self):
    dates_list = [(123, '2020-01-01'), (135, '2020-01-03')]
    res_list = add_missing_dates(dates_list)
    expected_list = [(123, '2020-01-01'), (123, '2020-01-02'), (135, '2020-01-03')]
    self.assertEqual(res_list, expected_list)
