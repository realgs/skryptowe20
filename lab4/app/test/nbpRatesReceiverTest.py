import unittest
from datetime import date

from lab4.app.src.nbpRatesReceiver import process_nbp_api_response


class NbpRatesReceiverTests(unittest.TestCase):
    def test_process_nbp_api_response(self):
        start_date = date(2020, 11, 5)
        nbp_response = {
            'table': 'A',
            'currency': 'dolar amerykański',
            'code': 'USD',
            'rates': [
                {'no': '217/A/NBP/2020', 'effectiveDate': '2020-11-05', 'mid': 3.8353},
                {'no': '218/A/NBP/2020', 'effectiveDate': '2020-11-06', 'mid': 3.8194}
            ]
        }
        expected_result = {
            'currency': 'USD',
            'rates': [
                {'date': '2020-11-05', 'rate': 3.8353},
                {'date': '2020-11-06', 'rate': 3.8194}
            ]
        }
        result = process_nbp_api_response(nbp_response, start_date)
        self.assertEqual(expected_result, result)

    def test_process_empty_nbp_api_response(self):
        start_date = date(2020, 11, 5)
        nbp_response = {
            'table': 'A',
            'currency': 'dolar amerykański',
            'code': 'USD',
            'rates': []
        }
        expected_result = {
            'currency': 'USD',
            'rates': []
        }
        result = process_nbp_api_response(nbp_response, start_date)
        self.assertEqual(expected_result, result)
