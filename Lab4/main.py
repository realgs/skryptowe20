from fetcher import get_avg_rates
from plotter import draw_plot

def main():
    usd_rates = get_avg_rates("USD", 180)
    # eur_rates = get_avg_rates("EUR", 180)

    # for r in usd_rates:
    #     print(f"USD on day {r.effective_date}: {r.mid}")

    draw_plot(usd_rates)
    
    # for r in eur_rates:
    #     print(f"EUR on day {r.effective_date}: {r.mid}")

if __name__ == "__main__":
    main()