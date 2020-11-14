import unittest
from datetime import date, timedelta

from ApiService import getAverageExchangeRatesInDays
from Exceptions.ApiError import ApiError


class GetAverageExchangeRatesInDaysTests(unittest.TestCase):
    def testFuncReturnsListFromTableA(self):
        returnData = getAverageExchangeRatesInDays("USD", 100)
        self.assertEqual(type(returnData), list)

    def testFuncReturnsListFromTableB(self):
        returnData = getAverageExchangeRatesInDays("AFN", 100)
        self.assertEqual(type(returnData), list)

    def testFuncFirstValueDateAfterInputDate(self):
        returnData = getAverageExchangeRatesInDays("USD", 100)
        startDate = date.today() - timedelta(days=100)
        firstDateStr = returnData[0]["effectiveDate"]
        firstDateSplited = firstDateStr.split("-")
        firstDate = date(int(firstDateSplited[0]), int(firstDateSplited[1]), int(firstDateSplited[2]))
        self.assertGreaterEqual(firstDate, startDate)

    def testFuncRisesErrorForIncorrectInputs(self):
        self.assertRaises(ApiError, getAverageExchangeRatesInDays, "12345", 10)
        self.assertRaises(ApiError, getAverageExchangeRatesInDays, "USD", -4)
        self.assertRaises(ApiError, getAverageExchangeRatesInDays, "AFN", 600)


if __name__ == '__main__':
    unittest.main()
