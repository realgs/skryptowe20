import lab4.rozwiazanie.sales as sales
import lab4.rozwiazanie.nbp as nbp
import lab4.rozwiazanie.work_with_db as work_with_db

if __name__ == '__main__':
    nbp.print_plot_for_dollar_euro_x_days(183)
    work_with_db.create_table_with_exchange_rates()
    sales.print_plot_with_sales_data('2003-10-01', '2004-07-07')
