import db_init
import data


def main():
    db_init.init_db()
    currency_data = data.get_currency_from_period('usd', date_from='2004-05-06', date_to='2005-05-07')
    print(currency_data)
    db_init.add_curr_rate_table(currency_data)


    # NA KOŃCU BIORĘ Z REQUESTA COŚ TAM COŚ TAM TAKE DATE, SUMA_ZYSKU ORDER BY DATA


main()