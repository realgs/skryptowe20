import nbp

def main():
    print(nbp.get_avg_ex_rate("EUR", 5))
    dollars, euros = nbp.get_dollar_euro_half_year()
    nbp.plot_dollar_euro(dollars, euros)
if __name__ == "__main__":
    main()