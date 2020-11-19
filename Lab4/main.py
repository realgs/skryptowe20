from fetcher import get_avg_rates
from plotter import draw_plot
from database_operations import add_table_currency_mids

def main():
    currencies = ["USD", "EUR"]
    days = 360 * 3
    # Zad 1, 2
    result = get_avg_rates(currencies, days)
    # Zad 3
    # draw_plot(result)
    # Zad 3
    add_table_currency_mids(result[0])
    # Zad 4

if __name__ == "__main__":
    main()
