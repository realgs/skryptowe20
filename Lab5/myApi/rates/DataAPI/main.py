from fetcher import get_avg_rates
from plotter import draw_list_of_wrappers
from database_operations import \
    add_table_currency_mids, \
    summarise_transactions
from constants import \
    PLOT_YAXIS_LABEL_TRANSACTIONS,\
    PLOT_TITLE_TRANSACTIONS

def main():
    currencies = ["USD", "EUR"]
    days = 365 * 3

    # Zad 1, 2
    # list_of_wrappers = get_avg_rates(currencies, days)

    # # Zad 3
    # draw_list_of_wrappers(list_of_wrappers)

    # # Zad 3
    # add_table_currency_mids(list_of_wrappers[0]) # wrapper at index 0 is USD currency

    # # Zad 4
    # result = summarise_transactions(currencies[0])
    # draw_list_of_wrappers(result, title=PLOT_TITLE_TRANSACTIONS,
    #                       yaxis=PLOT_YAXIS_LABEL_TRANSACTIONS)

if __name__ == "__main__":
    main()
