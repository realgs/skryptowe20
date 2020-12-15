from ccy_data import *


def add_table(conn, usd_to_pln_daily: pd.DataFrame):
    usd_to_pln_daily.to_sql(USD_EX_RATES_TABLE_NAME, conn, if_exists='replace')


usd_daily_ex_rates_df = get_complete_usd_daily_ex_rates(DATA_DATE_RANGE_START, DATA_DATE_RANGE_END)
usd_daily_ex_rates_df.sort_values('effectiveDate', inplace=True)

db_conn = get_db_connection(PATH_TO_DB)
add_table(db_conn, usd_daily_ex_rates_df)
