import lab5.db_service as db_service


def init():
    db_service.create_table_with_exchange_rates()
    db_service.create_sales_table()


if __name__ == '__main__':
    init()