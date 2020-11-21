import utilities


if __name__ == "__main__":
    usd_data = utilities.call_nbp_api_for("usd", "a", last_days = 186)
    eur_data = utilities.call_nbp_api_for("eur", "a", from_date = "2020-05-20")
    utilities.crate_two_currencies_graph("usd", usd_data, "eur", eur_data)
    utilities.create_database("2006-10-01", "2017-09-29")
    utilities.create_sales_graph(ResidentialType="Single Family")
