import pytest
import requests
from datetime import datetime, timedelta
from utilities_api import universal_database_rates_call
from utilities_nbp import to_date
from utilities_database import TODAY


BASES_RATES = ["http://127.0.0.1:5000/rates",
               "http://127.0.0.1:5000/rates/inter"]
BASE_SALES = "http://127.0.0.1:5000/sales"
CURRENCIES = ["usd", "eur", "huf", "chf", "gbp", "jpy", "czk", "aed", "bob"]
SINGLE_OK_DAYS = ["2020-11-17", "2020-04-22", "2003-05-20", "2004-10-26",
                  "2007-06-26", "2007-11-08", "2010-10-05", "2011-06-03",
                  "2011-12-12", "2012-04-24", "2012-09-12", "2014-09-16",
                  "2015-06-16", "2017-09-20", "2019-10-03", "2020-08-27"]
SINGLE_NOT_OK_DAYS = ["2020-11-11", "2020-04-11", "2002-11-09", "2020-12-20",
                      "2005-12-10", "2006-12-10", "2008-05-25", "2009-07-25",
                      "2015-01-03", "2015-03-07", "2015-11-28", "2016-02-27",
                      "2017-03-26", "2018-06-24", "2019-02-23", "2009-08-02"]
UNUSUAL_CASES = [
    ("2020-11-06", "2020-11-16", 11),
    ("2020-11-07", "2020-11-16", 10),
    ("2020-11-08", "2020-11-16", 9),
    ("2020-11-09", "2020-11-16", 8),
    ("2020-11-06", "2020-11-15", 10),
    ("2020-11-07", "2020-11-15", 9),
    ("2020-11-08", "2020-11-15", 8),
    ("2020-11-09", "2020-11-15", 7),
    ("2020-11-06", "2020-11-14", 9),
    ("2020-11-07", "2020-11-14", 8),
    ("2020-11-08", "2020-11-14", 7),
    ("2020-11-09", "2020-11-14", 6),
    ("2020-02-26", "2020-03-04", 8),
    ("2019-02-26", "2019-03-05", 8)
]
STANDARD_CASES = [
    ("2020-11-02", "2020-11-06", 5),
    ("2020-11-09", "2020-11-13", 5),
    ("2020-07-20", "2020-07-24", 5),
    ("2020-07-27", "2020-07-31", 5)
]
REAL_ESTATE_CASES = [
    ("2007-01-01", "2008-01-01"),
    ("2007-01-01", "2009-01-01"),
    ("2007-01-01", "2010-01-01"),
    ("2007-01-01", "2011-01-01"),
    ("2007-01-01", "2012-01-01"),
    ("2007-01-01", "2013-01-01"),
    ("2007-01-01", "2014-01-01"),
    ("2007-01-01", "2015-01-01"),
    ("2007-01-01", "2016-01-01"),
    ("2007-01-01", "2017-01-01")
]
SINGLE_DAY_SALES = [
    "2016-11-11", "2015-04-11", "2014-11-09", "2015-12-20",
    "2015-12-10", "2016-12-10", "2017-05-25", "2008-07-25",
    "2015-01-03", "2015-03-07", "2015-11-28", "2016-02-27",
    "2017-03-26", "2013-06-24", "2014-02-23", "2009-08-02"
]
LAST_DAY_CASES = [x for x in range(1, 100)]
SUPER_LONG_CASES = [x for x in range(350, 1350, 10)]


@pytest.mark.parametrize("code", CURRENCIES)
@pytest.mark.parametrize("single_day", SINGLE_OK_DAYS + SINGLE_NOT_OK_DAYS)
@pytest.mark.parametrize("base", BASES_RATES)
def test_single_days(single_day, code, base):
    response = requests.get(base + f"/{code}/{single_day}")
    result = response.json()[0]
    assert result["date"] == single_day
    assert result["rate"] is not None
    if "inter" in base:
        assert result["interpolated"] in [0, 1]


@pytest.mark.parametrize("code", CURRENCIES)
@pytest.mark.parametrize("from_date", SINGLE_OK_DAYS + SINGLE_NOT_OK_DAYS)
@pytest.mark.parametrize("base", BASES_RATES)
def test_from_date_till_today(from_date, code, base):
    response = requests.get(base + f"/{code}/{from_date}/today")
    check_exchange_rates(response.json(), from_date, TODAY(), base)


@pytest.mark.parametrize("code", CURRENCIES)
@pytest.mark.parametrize("case", UNUSUAL_CASES+STANDARD_CASES)
@pytest.mark.parametrize("base", BASES_RATES)
def test_from_date_till_date(case, code, base):
    response = requests.get(base + f"/{code}/{case[0]}/{case[1]}")
    check_exchange_rates(response.json(), case[0], case[1], base)


@pytest.mark.parametrize("code", CURRENCIES)
@pytest.mark.parametrize("last_days", LAST_DAY_CASES + SUPER_LONG_CASES)
@pytest.mark.parametrize("base", BASES_RATES)
def test_last_days(last_days, code, base):
    response = requests.get(base + f"/{code}/{last_days}")
    from_date = to_date(TODAY()) - timedelta(days=last_days-1)
    from_date = from_date.strftime('%Y-%m-%d')
    check_exchange_rates(response.json(), from_date, TODAY(), base)


@pytest.mark.parametrize("code", CURRENCIES[1:])
@pytest.mark.parametrize("single_day", SINGLE_DAY_SALES)
def test_sales_from_single_date(code, single_day):
    response = requests.get(BASE_SALES + f"/{code}/{single_day}")
    check_sales_rates(response.json(), single_day, single_day, code)


@pytest.mark.parametrize("code", CURRENCIES[1:])
@pytest.mark.parametrize("case", REAL_ESTATE_CASES)
def test_sales_from_date_till_date(code, case):
    response = requests.get(BASE_SALES + f"/{code}/{case[0]}/{case[1]}")
    check_sales_rates(response.json(), case[0], case[1], code)


@pytest.mark.parametrize("single_day", SINGLE_DAY_SALES)
def test_sales_from_single_date_to_pln(single_day):
    response = requests.get(BASE_SALES + f"/pln/{single_day}")
    check_sales_rates(response.json(), single_day, single_day, "PLN")


@pytest.mark.parametrize("case", REAL_ESTATE_CASES)
def test_sales_from_date_till_date_to_pln(case):
    response = requests.get(BASE_SALES + f"/pln/{case[0]}/{case[1]}")
    check_sales_rates(response.json(), case[0], case[1], "PLN")


def check_exchange_rates(result, from_date, till_date, base):
    expected_len = (to_date(till_date) - to_date(from_date)).days + 1
    assert len(result) == expected_len
    dates_list = [to_date(till_date) - timedelta(days=x) for x in range(expected_len)]
    for expected_date, actual_res in zip(sorted(dates_list), result):
        assert to_date(actual_res["date"]) == expected_date
        assert actual_res["rate"] is not None
        if "inter" in base:
            assert actual_res["interpolated"] in [0, 1]


def check_sales_rates(result, from_date, till_date, code):
    expected_len = (to_date(till_date) - to_date(from_date)).days + 1
    assert len(result) == expected_len
    dates_list = [to_date(till_date) - timedelta(days=x) for x in range(expected_len)]
    usds = requests.get(BASES_RATES[0] + f"/usd/{from_date}/{till_date}")
    usd_rates = [x["rate"] for x in usds.json()]
    if code != "PLN":
        bufs = requests.get(BASES_RATES[0] + f"/{code}/{from_date}/{till_date}")
        buf_rates = [x["rate"] for x in bufs.json()]
    else:
        buf_rates = [None]*expected_len
    for actual, usd_rate, buf_rate, date in zip(result, usd_rates, buf_rates, sorted(dates_list)):
        assert actual["USD rate"] == usd_rate 
        assert to_date(actual["Date"]) == date
        if code != "PLN":
            buf_sales = round(actual["USD sales"] * usd_rate / buf_rate, 2)
            assert actual[f"{code.upper()} rate"] == buf_rate
            assert actual[f"{code.upper()} sales"] == pytest.approx(buf_sales, 0.01)
        else:
            buf_sales = round(actual["USD sales"] * usd_rate, 2)
            assert actual[f"PLN sales"] == pytest.approx(buf_sales, 0.01)
