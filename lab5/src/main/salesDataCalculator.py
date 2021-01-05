from decimal import Decimal


def calculate_daily_orders_pln(daily_orders):
    total_amount_pln = Decimal('0.00')
    for order in daily_orders:
        total_amount_pln += order['totalAmount']
    return total_amount_pln


class SalesDataCalculator:

    def __init__(self, dao, rates_supplier):
        self.dao = dao
        self.rates_supplier = rates_supplier
        self.cache = {}

    def calculate_sales_amount(self, currency_code, date):
        daily_calcs = self.get_daily_calculations(date)
        return self.get_daily_calculations_in_currency(daily_calcs, currency_code, date)

    # Price in pln is calculated only once. Then it is taken from cache
    def get_daily_calculations(self, date):
        daily_calc = self.cache.get(date)
        if daily_calc is None:
            orders = self.dao.read_orders(date, date)
            daily_orders_pln_amount = calculate_daily_orders_pln(orders)
            new_daily_calc = {"PLN": daily_orders_pln_amount}
            self.cache[date] = new_daily_calc
            return new_daily_calc
        else:
            return daily_calc

    # Price in given currency is calculated only once. Then it is taken from cache
    def get_daily_calculations_in_currency(self, daily_calcs, currency_code, date):
        daily_calc_in_currency = daily_calcs.get(currency_code)
        if daily_calc_in_currency is None:
            daily_calc_in_pln = daily_calcs['PLN']
            currency_rates = self.rates_supplier(currency_code, date)
            currency_rate = Decimal(str(currency_rates['rates'][0]['rate']))
            new_calc_in_currency = daily_calc_in_pln / currency_rate
            daily_calcs[currency_code] = new_calc_in_currency
            return new_calc_in_currency
        else:
            return daily_calc_in_currency
