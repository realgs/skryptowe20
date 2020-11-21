import pytest
import utilities
import os


TABLE_A_CURRENCIES = ["thb", "usd", "aud", "hkd", "cad", "nzd", "sgd", "eur",
                      "huf", "chf", "gbp", "uah", "jpy", "czk", "dkk", "isk",
                      "nok", "sek", "hrk", "ron", "bgn", "try", "ils", "clp",
                      "php", "mxn", "zar", "brl", "myr", "rub", "idr", "inr",
                      "krw", "xdr"]

TABLE_B_CURRENCIES = ['afn', 'mga', 'pab', 'etb', 'ves', 'bob', 'crc', 'svc',
                      'nio', 'gmd', 'mkd', 'dzd', 'bhd', 'iqd', 'jod', 'kwd',
                      'lyd', 'rsd', 'tnd', 'mad', 'zea', 'aed', 'stn', 'bsd',
                      'bbd', 'bzd', 'bnd', 'fjd', 'gyd', 'jmd', 'lrd', 'nad',
                      'srd', 'ttd', 'xcd', 'sbd', 'zwl', 'vnd', 'amd', 'cve',
                      'awg', 'bif', 'xof', 'xaf', 'xpf', 'djf', 'gnf', 'kmf',
                      'cdf', 'rwf', 'egp', 'gip', 'lbp', 'ssp', 'sdg', 'syp',
                      'ghs', 'htg', 'pyg', 'ang', 'pgk', 'lak', 'mwk', 'zmw',
                      'aoa', 'mmk', 'gel', 'mdl', 'all', 'hnl', 'sll', 'szl',
                      'lsl', 'azn', 'mzn', 'ngn', 'ern', 'twd', 'tmt', 'mru',
                      'mop', 'ars', 'dop', 'cop', 'cup', 'uyu', 'bwp', 'gtq',
                      'irr', 'yer', 'qar', 'omr', 'sar', 'khr', 'byn', 'lkr',
                      'mvr', 'mur', 'npr', 'pkr', 'scr', 'pen', 'kgs', 'tjs',
                      'uzs', 'kes', 'sos', 'tzs', 'ugx', 'bdt', 'wst', 'kzt',
                      'mnt', 'vuv', 'bam']

SIMPLE_CURRENCIES = [("usd", "a"), ("eur", "a"), ("gbp", "a")]
TABLE_A_CURRENCIES = [(x, "a") for x in TABLE_A_CURRENCIES]
TABLE_B_CURRENCIES = [(x, "b") for x in TABLE_B_CURRENCIES]

SINGLE_OK_DAYS = ["2020-11-17", "2020-04-22", "2003-05-20", "2004-10-26",
                  "2007-06-26", "2007-11-08", "2010-10-05", "2011-06-03",
                  "2011-12-12", "2012-04-24", "2012-09-12", "2014-09-16",
                  "2015-06-16", "2017-09-20", "2019-10-03", "2020-08-27"]

SINGLE_NOT_OK_DAYS = ["2020-11-11", "2020-04-11", "2002-11-09", "2005-07-10",
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

LAST_DAY_CASES = [x for x in range(1, 100)]
SUPER_LONG_CASES = [x for x in range(350, 1350, 10)]


@pytest.mark.parametrize("currency", TABLE_A_CURRENCIES + TABLE_B_CURRENCIES)
@pytest.mark.parametrize("single_day", SINGLE_OK_DAYS)
def test_single_ok_days(single_day, currency):
    result = utilities.call_nbp_api_for(
        currency[0], currency[1], from_date=single_day, till_date=single_day)
    assert isinstance(result, dict)


@pytest.mark.parametrize("currency", TABLE_A_CURRENCIES + TABLE_B_CURRENCIES)
@pytest.mark.parametrize("single_not_ok_day", SINGLE_NOT_OK_DAYS)
def test_single_not_ok_days(single_not_ok_day, currency):
    result = utilities.call_nbp_api_for(
        currency[0], currency[1], from_date=single_not_ok_day, till_date=single_not_ok_day)
    assert isinstance(result, dict)


@pytest.mark.parametrize("currency", TABLE_A_CURRENCIES + TABLE_B_CURRENCIES)
@pytest.mark.parametrize("case", UNUSUAL_CASES+STANDARD_CASES)
def test_unusual_and_standard_cases(case, currency):
    from_date, till_date, expected_number_of_results = case
    result = utilities.call_nbp_api_for(
        currency[0], currency[1], from_date=from_date, till_date=till_date)
    assert len(result) == expected_number_of_results
    assert None not in result.values()


@pytest.mark.parametrize("currency", TABLE_A_CURRENCIES + TABLE_B_CURRENCIES)
@pytest.mark.parametrize("last_day_number", LAST_DAY_CASES + SUPER_LONG_CASES)
def test_last_days(last_day_number, currency):
    result = utilities.call_nbp_api_for(
        currency[0], currency[1], last_days=last_day_number)
    assert len(result) == last_day_number
    assert None not in result.values()


@pytest.mark.parametrize("currency_1", SIMPLE_CURRENCIES)
@pytest.mark.parametrize("currency_2", SIMPLE_CURRENCIES)
@pytest.mark.parametrize("case", UNUSUAL_CASES + STANDARD_CASES)
def test_create_svg_rates_plot(currency_1, currency_2, case):
    if os.path.isfile(utilities.SVG_RATES):
        os.remove(utilities.SVG_RATES)
    from_date, till_date, _ = case
    results_1 = utilities.call_nbp_api_for(
        currency_1[0], currency_1[1], from_date=from_date, till_date=till_date)
    results_2 = utilities.call_nbp_api_for(
        currency_2[0], currency_2[1], from_date=from_date, till_date=till_date)
    utilities.crate_two_currencies_graph(
        currency_1[0], results_1, currency_2[0], results_2)
    assert os.path.isfile(utilities.SVG_RATES)


@pytest.mark.parametrize("case", REAL_ESTATE_CASES)
def test_create_svg_real_estate_plot(case):
    if os.path.isfile(utilities.SVG_REAL_ESTATE):
        os.remove(utilities.SVG_REAL_ESTATE)
    utilities.create_database(case[0], case[1])
    utilities.create_sales_graph()
    assert os.path.isfile(utilities.SVG_RATES)
