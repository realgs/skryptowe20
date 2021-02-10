import os
from datetime import datetime, timedelta
import requests
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoLocator, AutoMinorLocator, FormatStrFormatter
import sqlite3 as sql
import pandas as pd


API_URL = "http://api.nbp.pl/api/exchangerates/rates/{}/{}/{}/{}/"
FROM = "from_date"
TILL = "till_date"
SVG_RATES = os.path.join(os.path.dirname(__file__), "exchenge_graph.svg")
SVG_REAL_ESTATE = os.path.join(
    os.path.dirname(__file__), "real_estate_graph.svg")
SALES_DATA_PATH = os.path.join(
    os.path.dirname(__file__), "real_estate_sales.csv")
DB_PATH = os.path.join(os.path.dirname(__file__), "my_db.db")
DEFAULT_FIG_SIZE = (13, 7)
BIG_FIG_SIZE = (26, 14)
LABEL_X_TIME = "Time"
LABEL_Y_PRICE_IN_PLN = "Price in PLN"
LABEL_Y_REAL_ESTATE_PRICE = "Price in USD/PLN"
RATES_TITLE = "Prices of {} and {} through time. From {} to {}"
REAL_ESTATE_TITLE = "Sales of real estate in USD and PLN through time. From {} to {}"
LABLE_FONTSIZE = 15
TITLE_FONTSIZE = 20
LEGEND_FONTSIZE = 13
THICCNESSES = (2, 7, 4)
LABEL_FONTSTYLE = "italic"
TITLE_FONTWEIGHT = "bold"
AVG_SEL = "AVG(SaleAmount)"
AVG_SEL_MID = AVG_SEL + "*mid"
DATE_COL = "DateRecorded"
PLN_TABLE_NAME = "pln_rates"
SALES_TABLE_NAME = "sales"
COLUMNS_TO_DROP = ["ID", "SerialNumber", "ListYear", "NonUseCode", "Remarks"]
LAST_DAYS_TO_CHECK = 14
DEFAULT_ERR_MSG = "Cannot figure out these arguments: {} {} {} {}"


def call_nbp_api_for(currency, table, **kwargs):
    from_date, till_date = change_kwargs_to_two_days(kwargs, currency, table)

    dt_till = datetime.combine(till_date, datetime.min.time())
    dt_from = datetime.combine(from_date, datetime.min.time())
    if (dt_till-dt_from).days > 365:
        return split_api_calls(from_date, till_date, currency, table)

    till_date = str(till_date)
    from_date = str(from_date)
    link = API_URL.format(table, currency, from_date, till_date)
    nbp_req = requests.get(link)

    result = {}
    if nbp_req.status_code == 200:
        for buf in nbp_req.json()["rates"]:
            result[buf["effectiveDate"]] = buf["mid"]
    elif nbp_req.status_code == 404 and till_date == from_date and "repeating" not in kwargs:
        for i in range(LAST_DAYS_TO_CHECK):
            buf_day = to_date(till_date) - timedelta(days=i)
            buf_result = call_nbp_api_for(
                currency, table, from_date=buf_day, till_date=buf_day, repeating=i)
            if isinstance(buf_result, dict):
                return buf_result
        raise ValueError(DEFAULT_ERR_MSG.format(
            currency, table, from_date, till_date))
    elif "repeating" not in kwargs:
        raise ValueError(DEFAULT_ERR_MSG.format(
            currency, table, from_date, till_date))
    else:
        return

    return repair_exchange_data(result, from_date, till_date, currency, table)


def change_kwargs_to_two_days(kwargs, currency, table):
    if "last_days" in kwargs:
        kwargs[TILL] = datetime.date(datetime.now())
        kwargs[FROM] = kwargs[TILL] - timedelta(kwargs["last_days"] - 1)
    elif FROM in kwargs and TILL in kwargs:
        kwargs[TILL] = to_date(kwargs[TILL])
        kwargs[FROM] = to_date(kwargs[FROM])
    elif FROM in kwargs:
        kwargs[TILL] = datetime.date(datetime.now())
        kwargs[FROM] = to_date(kwargs[FROM])
    else:
        raise ValueError(DEFAULT_ERR_MSG.format(currency, table, kwargs))
    return kwargs[FROM], kwargs[TILL]


def split_api_calls(from_date, till_date, currency, table):
    periods = [[from_date, None]]
    counter = 0
    while True:
        from_date += timedelta(days=365)
        if from_date > till_date:
            break
        else:
            periods[counter][1] = from_date - timedelta(days=1)
            counter += 1
            periods.append([from_date, None])
    periods[counter][1] = till_date

    total_result = {}
    for p in periods:
        buf_res = call_nbp_api_for(
            currency, table, from_date=p[0], till_date=p[1])
        total_result.update(buf_res)
    return total_result


def repair_exchange_data(nbp_data, first_day, last_day, currency, table):
    new_data = nbp_data.copy()
    if first_day == last_day:
        return new_data

    buf_day = to_date(first_day)
    while buf_day <= to_date(last_day):
        str_buf_day = str(buf_day)
        if str_buf_day not in new_data:
            new_data[str_buf_day] = None
        buf_day += timedelta(days=1)

    for key, val in new_data.items():
        if not val:
            previous_day = to_date(key) - timedelta(days=1)
            if str(previous_day) in new_data.keys():
                new_data[key] = new_data[str(previous_day)]

    new_data = dict(sorted(new_data.items()))
    if None in new_data.values():
        buf_result = call_nbp_api_for(
            currency, table, from_date=first_day, till_date=first_day)
        missing_mid = list(buf_result.values())[0]
        for key, val in new_data.items():
            if not val:
                new_data[key] = missing_mid
            else:
                break

    return new_data


def crate_two_currencies_graph(curr_1, data_1, curr_2, data_2):
    (dates_1, mids_1) = zip(*data_1.items())
    (dates_2, mids_2) = zip(*data_2.items())
    rates_title = RATES_TITLE.format(
        curr_1.upper(), curr_2.upper(), dates_1[0], dates_1[-1])
    init_graph(dates_1, mids_1, dates_2, mids_2, DEFAULT_FIG_SIZE,
               LABEL_X_TIME, LABEL_Y_PRICE_IN_PLN, rates_title, SVG_RATES)


def create_sales_graph(**kwargs):
    select_cmd = init_select_command(kwargs)
    conn = sql.connect(DB_PATH)
    output = pd.read_sql(select_cmd, conn)
    conn.close()
    real_estate_title = REAL_ESTATE_TITLE.format(
        output[DATE_COL].iloc[0], output[DATE_COL].iloc[-1])
    init_graph(output[DATE_COL], output[AVG_SEL], output[DATE_COL],
               output[AVG_SEL_MID], BIG_FIG_SIZE, LABEL_X_TIME,
               LABEL_Y_REAL_ESTATE_PRICE, real_estate_title, SVG_REAL_ESTATE)


def init_graph(x1, y1, x2, y2, fig_size, label_x, label_y, title, output_path, legend=["USD", "PLN"]):
    _, ax = plt.subplots(figsize=fig_size)
    ax.plot(x1, y1)
    ax.plot(x2, y2)
    ax.xaxis.set_major_locator(AutoLocator())
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_major_locator(AutoLocator())
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.tick_params(which='both', width=THICCNESSES[0])
    ax.tick_params(which='major', length=THICCNESSES[1])
    ax.tick_params(which='minor', length=THICCNESSES[2])
    ax.set_xlabel(label_x, fontstyle=LABEL_FONTSTYLE, fontsize=LABLE_FONTSIZE)
    ax.set_ylabel(label_y, fontstyle=LABEL_FONTSTYLE, fontsize=LABLE_FONTSIZE)
    ax.set_title(title, fontsize=TITLE_FONTSIZE, fontweight=TITLE_FONTWEIGHT)
    ax.legend(legend, fontsize=LEGEND_FONTSIZE)
    plt.grid(True)
    plt.savefig(output_path)


def create_database(from_date, till_date):
    if os.path.isfile(DB_PATH):
        conn = sql.connect(DB_PATH)
    else:
        conn = init_database_from_csv()
    add_pln_table(conn, from_date, till_date)
    conn.commit()
    conn.close()


def init_database_from_csv():
    sales = pd.read_csv(SALES_DATA_PATH).dropna()
    sales = sales.infer_objects()
    sales[DATE_COL] = pd.to_datetime(
        sales[DATE_COL], errors="coerce", infer_datetime_format=True)
    sales[DATE_COL] = sales[DATE_COL].astype(str)
    sales = sales.drop(columns=COLUMNS_TO_DROP)
    conn = sql.connect(DB_PATH)
    sales.to_sql(SALES_TABLE_NAME, conn)
    return conn


def add_pln_table(conn, from_date, till_date):
    c = conn.cursor()
    c.execute(f'DROP TABLE IF EXISTS {PLN_TABLE_NAME}')
    c.execute(f'CREATE TABLE {PLN_TABLE_NAME} (date text, mid real)')
    pln_data = call_nbp_api_for(
        "usd", "a", from_date=from_date, till_date=till_date)
    (pln_dates, pln_mids) = zip(*pln_data.items())
    pln_data = [(x, y) for x, y in zip(pln_dates, pln_mids)]
    c.executemany(f'INSERT INTO {PLN_TABLE_NAME} VALUES (?,?)', pln_data)


def init_select_command(extra_args):
    select_cmd = 'SELECT {}, {}, {} FROM {} JOIN {} ON date = {}'
    select_cmd = select_cmd.format(AVG_SEL, AVG_SEL_MID, DATE_COL,
                                   SALES_TABLE_NAME, PLN_TABLE_NAME, DATE_COL)
    for key, value in extra_args.items():
        select_cmd += f' AND "{key}"'
        if isinstance(value, list):
            select_cmd += ' IN ('
            select_cmd += ','.join(f"'{x}'" for x in value)
            select_cmd += ')'
        else:
            select_cmd += f" = '{value}'"
    select_cmd += f' GROUP BY {DATE_COL} ORDER BY {DATE_COL}'
    return select_cmd


def to_date(date):
    return datetime.strptime(str(date), '%Y-%m-%d').date()
