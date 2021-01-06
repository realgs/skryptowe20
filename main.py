import nbp
import db
import datetime


def nbp_rates_test():
    dates = []
    rateseur = []
    ratesusd = []
    resp = nbp.get_avg_rates('EUR', 120)
    print("Pobrano kursy EUR z ostatnich 120 dni:")
    for item in resp:
        dates.append(datetime.datetime.strptime(item['effectiveDate'], "%Y-%m-%d"))
        rateseur.append(item['mid'])
        print('{} {}'.format(item['effectiveDate'], item['mid']))
    resp = nbp.get_avg_rates('USD', 120)
    print("Pobrano kursy USD z ostatnich 120 dni:")
    for item in resp:
        ratesusd.append(item['mid'])
        print('{} {}'.format(item['effectiveDate'], item['mid']))
    nbp.plot(rateseur, ratesusd, 'EUR', 'USD', dates)


def db_rates_test():
    database = r"C:\Users\Patrycja\Desktop\5 semestr\Języki skryptowe\salesData.db"
    conn = db.create_connection(database)
    with conn:
        print('Mamy połączenie')
        db.select_data_and_plot(conn)


if __name__ == '__main__':
    nbp_rates_test()
    db_rates_test()
