from datetime import datetime, timedelta

from currency_data import get_currencies_data

USD_PRICES_TABLE_NAME = 'USDPrices'


def get_complete_usd_to_pln_data(start_date, end_date):
    catchup = (end_date - start_date).days + 1
    usd_to_pln_daily = get_currencies_data(['USD'], catchup, end_date)

    ref_price = usd_to_pln_daily.loc[usd_to_pln_daily.index[0]]['USD']

    for single_date in ((start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(catchup)):
        if single_date not in usd_to_pln_daily.index:
            usd_to_pln_daily.loc[single_date] = ref_price
        else:
            ref_price = usd_to_pln_daily.loc[single_date]['USD']
    usd_to_pln_daily.sort_index(inplace=True)

    return usd_to_pln_daily


if __name__ == '__main__':
    strt = datetime(2012, 8, 1)
    # strt = datetime(2014, 12, 13)
    end = datetime(2015, 1, 1)
    add_df = get_complete_usd_to_pln_data(strt, end)
    print(add_df)
