from fetcher import get_avg_rates
from plotter import draw_plot

def main():
    currencies = ["USD", "EUR"]
    days = 180

    result = get_avg_rates(currencies, days)

    draw_plot(result)

if __name__ == "__main__":
    main()