import unittest
from datetime import date

from main.validation import validate_rates_request, validate_sales_request


class RatesRequestValidationTest(unittest.TestCase):
    def test_proper_rates_validation(self):
        currency_code = 'USD'
        args = {
            'startDate': '2020-01-01',
            'endDate': '2020-01-01'
        }
        expected_params = {
            'currencyCode': 'USD',
            'startDate': date(2020, 1, 1),
            'endDate': date(2020, 1, 1)
        }
        is_proper_request, params_or_errors = validate_rates_request(currency_code, args)
        self.assertTrue(is_proper_request)
        self.assertEqual(expected_params, params_or_errors)

    def test_rates_validation_for_non_supported_currency(self):
        currency_code = 'ADS'
        args = {
            'startDate': '2020-01-01',
            'endDate': '2020-01-01'
        }
        is_proper_request, params_or_errors = validate_rates_request(currency_code, args)
        self.assertFalse(is_proper_request)

    def test_rates_validation_for_wrong_date(self):
        currency_code = 'USD'
        args = {
            'startDate': '2020-01-01',
            'endDate': 'dasasd'
        }
        is_proper_request, params_or_errors = validate_rates_request(currency_code, args)
        self.assertFalse(is_proper_request)

    def test_rates_validation_for_no_dates(self):
        currency_code = 'USD'
        args = {}
        is_proper_request, params_or_errors = validate_rates_request(currency_code, args)
        self.assertFalse(is_proper_request)

    def test_rates_validation_for_start_date_greater_then_end_date(self):
        currency_code = 'USD'
        args = {
            'startDate': '2020-01-02',
            'endDate': '2020-01-01',
        }
        is_proper_request, params_or_errors = validate_rates_request(currency_code, args)
        self.assertFalse(is_proper_request)

    def test_rates_validation_for_too_early_dates(self):
        currency_code = 'USD'
        args = {
            'startDate': '2010-01-02',
            'endDate': '20210-01-20',
        }
        is_proper_request, params_or_errors = validate_rates_request(currency_code, args)
        self.assertFalse(is_proper_request)

    def test_rates_validation_for_too_big_days_delta(self):
        currency_code = 'USD'
        args = {
            'startDate': '2018-01-02',
            'endDate': '2019-02-20',
        }
        is_proper_request, params_or_errors = validate_rates_request(currency_code, args)
        self.assertFalse(is_proper_request)


class SalesRequestValidationTest(unittest.TestCase):
    def test_proper_sales_validation(self):
        currency_code = 'USD'
        args = {
            'date': '2020-01-01'
        }
        expected_params = {
            'currencyCode': 'USD',
            'date': date(2020, 1, 1),
        }
        is_proper_request, params_or_errors = validate_sales_request(currency_code, args)
        self.assertTrue(is_proper_request)
        self.assertEqual(expected_params, params_or_errors)

    def test_rates_validation_for_non_supported_currency(self):
        currency_code = 'USDADS'
        args = {
            'date': '2020-01-01'
        }
        is_proper_request, params_or_errors = validate_sales_request(currency_code, args)
        self.assertFalse(is_proper_request)

    def test_rates_validation_for_wrong_date(self):
        currency_code = 'USD'
        args = {
            'date': '202aasd-123-123',
        }
        is_proper_request, params_or_errors = validate_sales_request(currency_code, args)
        self.assertFalse(is_proper_request)

    def test_rates_validation_for_no_dates(self):
        currency_code = 'USD'
        args = {}
        is_proper_request, params_or_errors = validate_sales_request(currency_code, args)
        self.assertFalse(is_proper_request)

    def test_rates_validation_for_start_date_in_future(self):
        currency_code = 'USD'
        args = {
            'date': '2045-01-02',
        }
        is_proper_request, params_or_errors = validate_sales_request(currency_code, args)
        self.assertFalse(is_proper_request)

    def test_rates_validation_for_too_early_date(self):
        currency_code = 'USD'
        args = {
            'date': '2010-01-02',
        }
        is_proper_request, params_or_errors = validate_sales_request(currency_code, args)
        self.assertFalse(is_proper_request)
