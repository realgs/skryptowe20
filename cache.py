from datetime import timedelta
import time


class Cache():
    day_rates = {}
    day_sales = {}
    refresh_time = 3600 * 12
    time_start = time.time()

    def refresh_check(self):
        if time.time() - self.time_start > self.refresh_time:
            self.day_rates = {}
            self.day_sales = {}
            self.time_start = time.time()

    def has_rate(self, date):
        return date.strftime("%Y-%m-%d") in self.day_rates

    def has_rates_range(self, start_date, end_date):
        delta = timedelta(days=1)
        has_rates = True
        while start_date <= end_date:
            if start_date.strftime("%Y-%m-%d") not in self.day_rates:
                has_rates= False
            start_date += delta
        return has_rates

    def has_sale(self, date):
        return date.strftime("%Y-%m-%d") in self.day_sales

    def has_sales_range(self, start_date, end_date):
        delta = timedelta(days=1)
        has_sales = True
        while start_date <= end_date:
            if start_date.strftime("%Y-%m-%d") not in self.day_sales:
                has_sales = False
            start_date += delta
        return has_sales

    def get_rates_range(self, start_date, end_date):
        rates = {}
        delta = timedelta(days=1)
        while start_date <= end_date:
            rates[start_date.strftime("%Y-%m-%d")] = self.day_rates[start_date.strftime("%Y-%m-%d")]
            start_date += delta
        return rates

    def get_sales_range(self, start_date, end_date):
        sales = {}
        sumUSD = 0
        sumPLN = 0
        delta = timedelta(days=1)
        while start_date <= end_date:
            sales[start_date.strftime("%Y-%m-%d")] = self.day_sales[start_date.strftime("%Y-%m-%d")]
            sumUSD += self.day_sales[start_date.strftime("%Y-%m-%d")]["USD"]
            sumPLN += self.day_sales[start_date.strftime("%Y-%m-%d")]["PLN"]
            start_date += delta
        sales["sumUSD"] = sumUSD
        sales["sumPLN"] = sumPLN
        return sales
