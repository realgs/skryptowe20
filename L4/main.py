import datetime
import exchange_rates_api
import printing_chart
import sales_data_base


def modify_data_base(first_day, last_day, currency_code):
    exchange_rates_dict = exchange_rates_api.get_exchange_rates_from_to(first_day, last_day, currency_code)
    exchange_rates_dict = exchange_rates_api.complete_exchange_rates(first_day, last_day, exchange_rates_dict, currency_code)
    sales_data_base.create_exchange_rate_table()
    sales_data_base.insert_exchange_rates(exchange_rates_dict)


def print_sales_data(first_day, last_day, currency_code):
    sales_data = sales_data_base.get_sales_data(first_day, last_day)
    sales_curr_dict = {}
    sales_pln_dict = {}
    for item in sales_data:
        sales_curr_dict[item[0]] = item[1]
        sales_pln_dict[item[0]] = item[2]
    sales_dicts = [sales_curr_dict, sales_pln_dict]
    printing_chart.print_values_in_time(sales_dicts, ["USD", "PLN"], "wartość sprzedanych towarów", "Łączna sprzedaż")


if __name__ == "__main__":
    usd_exchange_rates = exchange_rates_api.get_exchange_rates_from_last_days(183, "USD")
    eur_exchange_rates = exchange_rates_api.get_exchange_rates_from_last_days(183, "EUR")
    printing_chart.print_values_in_time([eur_exchange_rates, usd_exchange_rates], ["EUR", "USD"], "śr. kurs [PLN]", "Średnie kursy walut")
    # modify_data_base(datetime.date(2013, 1, 1), datetime.date(2016, 12, 31), "USD")
    print_sales_data(datetime.date(2013, 1, 1), datetime.date(2016, 12, 31), "USD")
