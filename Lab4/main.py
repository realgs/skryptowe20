from fetcher import get_avg_rates

def main():
    usd_rates = get_avg_rates("USD", 6000)
    # eur_rates = get_avg_rates("EUR", 180)

    for r in usd_rates:
        print(f"USD on day {r.effective_date}: {r.mid}")

    # for r in eur_rates:
    #     print(f"EUR on day {r.effective_date}: {r.mid}")

if __name__ == "__main__":
    main()