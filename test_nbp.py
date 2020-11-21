import unittest
from nbp import get_dates, from_json_to_list

class TestNbp(unittest.TestCase):
  def test_get_dates_less_than_api_limit(self):
    start = '2018-01-01'
    end = '2018-05-01'
    dates = get_dates(start, end)
    self.assertEqual(dates, [start, end])


  def test_get_dates_more_than_api_limit(self):
    start = '2016-01-01'
    end = '2018-01-01'
    dates = get_dates(start, end)
    self.assertEqual(dates, ['2016-01-01', '2016-12-26', '2017-12-21', '2017-12-30'])


  def test_from_json_to_list(self):
    mid = 123
    date = '2020-01-01'
    json = {'rates': [{'mid': mid, 'effectiveDate': date}]}
    res_list = [(mid, date)]
    result = from_json_to_list(json)
    self.assertEqual(result, res_list)
