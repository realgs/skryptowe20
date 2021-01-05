import unittest
from datetime import date

from main.nbpRatesReceiver import process_nbp_api_response


class NbpRatesReceiverTests(unittest.TestCase):
    def test_process_nbp_api_response_without_interpolated_elements(self):
        start_date = date(2018, 5, 21)
        end_date = date(2018, 5, 23)

        nbp_response = {
            "table": "A",
            "currency": "dolar amerykański",
            "code": "USD",
            "rates": [
                {
                    "no": "094/A/NBP/2018",
                    "effectiveDate": "2018-05-16",
                    "mid": 3.6241
                },
                {
                    "no": "095/A/NBP/2018",
                    "effectiveDate": "2018-05-17",
                    "mid": 3.6283
                },
                {
                    "no": "096/A/NBP/2018",
                    "effectiveDate": "2018-05-18",
                    "mid": 3.6385
                },
                {
                    "no": "097/A/NBP/2018",
                    "effectiveDate": "2018-05-21",
                    "mid": 3.6615
                },
                {
                    "no": "098/A/NBP/2018",
                    "effectiveDate": "2018-05-22",
                    "mid": 3.6252
                },
                {
                    "no": "099/A/NBP/2018",
                    "effectiveDate": "2018-05-23",
                    "mid": 3.6693
                }
            ]
        }
        expected_result = {
            "currencyCode": "USD",
            "rates": [
                {
                    "date": date(2018, 5, 21),
                    "interpolated": False,
                    "rate": 3.6615
                },
                {
                    "date": date(2018, 5, 22),
                    "interpolated": False,
                    "rate": 3.6252
                },
                {
                    "date": date(2018, 5, 23),
                    "interpolated": False,
                    "rate": 3.6693
                }
            ]
        }
        result = process_nbp_api_response(nbp_response, start_date, end_date)
        self.assertEqual(expected_result, result)

    def test_process_nbp_api_date_with_weekend(self):
        start_date = date(2020, 11, 20)
        end_date = date(2020, 11, 23)

        nbp_response = {
            "table": "A",
            "currency": "dolar amerykański",
            "code": "USD",
            "rates": [
                {
                    "no": "223/A/NBP/2020",
                    "effectiveDate": "2020-11-16",
                    "mid": 3.7782
                },
                {
                    "no": "224/A/NBP/2020",
                    "effectiveDate": "2020-11-17",
                    "mid": 3.7877
                },
                {
                    "no": "225/A/NBP/2020",
                    "effectiveDate": "2020-11-18",
                    "mid": 3.7621
                },
                {
                    "no": "226/A/NBP/2020",
                    "effectiveDate": "2020-11-19",
                    "mid": 3.7872
                },
                {
                    "no": "227/A/NBP/2020",
                    "effectiveDate": "2020-11-20",
                    "mid": 3.7677
                },
                {
                    "no": "228/A/NBP/2020",
                    "effectiveDate": "2020-11-23",
                    "mid": 3.7616
                }
            ]
        }
        expected_result = {
            "currencyCode": "USD",
            "rates": [
                {
                    "date": date(2020, 11, 20),
                    "interpolated": False,
                    "rate": 3.7677
                },
                {
                    "date": date(2020, 11, 21),
                    "interpolated": True,
                    "rate": 3.7677
                },
                {
                    "date": date(2020, 11, 22),
                    "interpolated": True,
                    "rate": 3.7677
                },
                {
                    "date": date(2020, 11, 23),
                    "interpolated": False,
                    "rate": 3.7616
                }
            ]
        }
        result = process_nbp_api_response(nbp_response, start_date, end_date)
        self.assertEqual(expected_result, result)

    def test_process_nbp_api_for_single_weekend_day(self):
        start_date = date(2020, 11, 28)
        end_date = date(2020, 11, 28)
        nbp_response = {
            "table": "A",
            "currency": "dolar amerykański",
            "code": "USD",
            "rates": [
                {
                    "no": "100/A/NBP/2020",
                    "effectiveDate": "2020-05-25",
                    "mid": 4.1428
                },
                {
                    "no": "101/A/NBP/2020",
                    "effectiveDate": "2020-05-26",
                    "mid": 4.0885
                },
                {
                    "no": "102/A/NBP/2020",
                    "effectiveDate": "2020-05-27",
                    "mid": 4.0504
                }
            ]
        }
        expected_result = {
            "currencyCode": "USD",
            "rates": [
                {
                    "date": date(2020, 11, 28),
                    "interpolated": True,
                    "rate": 4.0504
                }
            ]
        }
        result = process_nbp_api_response(nbp_response, start_date, end_date)
        self.assertEqual(expected_result, result)

    def test_process_empty_nbp_api_response(self):
        start_date = date(2020, 11, 5)
        end_date = date(2020, 11, 5)

        nbp_response = {
            'table': 'A',
            'currency': 'dolar amerykański',
            'code': 'USD',
            'rates': []
        }
        expected_result = {
            'currencyCode': 'USD',
            'rates': []
        }
        result = process_nbp_api_response(nbp_response, start_date, end_date)
        self.assertEqual(expected_result, result)
