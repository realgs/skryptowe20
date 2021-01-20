import requests
import datetime as dtm
import matplotlib.pyplot as plt


def _url(path):
    return 'http://api.nbp.pl/api/' + path


def get_avg_rates_date(code, start, end):
    ret = []
    if type(start) != type(dtm.date.today()):
        fstdate = dtm.datetime.strptime(start, "%Y-%m-%d").date()
    else:
        fstdate = start
    if type(end) != type(dtm.date.today()):
        snddate = dtm.datetime.strptime(end, "%Y-%m-%d").date()
    else:
        snddate = end
    days = snddate - fstdate
    while days > dtm.timedelta(days=93):
        get = requests.get(
            _url('exchangerates/rates/A/{}/{}/{}/'.format(code, fstdate.strftime("%Y-%m-%d"),
                                                          (fstdate + dtm.timedelta(days=92)).strftime("%Y-%m-%d"))))
        if get.status_code != 200:
            print("Error : {}".format(get.status_code))
            return []
        ret += get.json()['rates']
        fstdate += dtm.timedelta(days=93)
        days = snddate - fstdate
    get = requests.get(
        _url(
            'exchangerates/rates/A/{}/{}/{}/'.format(code, fstdate.strftime("%Y-%m-%d"), snddate.strftime("%Y-%m-%d"))))
    if get.status_code != 200:
        print("Error {} ".format(get.status_code))
        return []
    ret += get.json()['rates']
    return ret


def get_avg_rates(code, days):
    return get_avg_rates_date(code, (dtm.date.today() - dtm.timedelta(days=days)), dtm.date.today())


def get_one_day_rate(code, date):
    get = requests.get(_url('exchangerates/rates/A/{}/{}/'.format(code, date)))
    if get.status_code != 200:
        print("Error: {}".format(get.status_code))
        return ()
    return get.json()['rates']


def get_closest_one_day_rate(code, date):
    get = requests.get(_url('exchangerates/rates/A/{}/{}/'.format(code, date)))
    if get.status_code != 200:
        if get.status_code == 404:
            datebefore = dtm.datetime.strptime(date, "%Y-%m-%d").date() - dtm.timedelta(days=1)
            date = datebefore.strftime("%Y-%m-%d")
            return get_closest_one_day_rate(code, date)
        else:
            print("Error: {} -->{}".format(get.status_code, _url('exchangerates/rates/A/{}/{}/'.format(code, date))))
            return []
    return get.json()['rates']


def plot(rates1, rates2, label1, label2, dates):
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(dates, rates1, label=label1)
    ax.plot(dates, rates2, label=label2)
    ax.set_title('Średni kurs walut z ostatnich 120 dni')
    ax.legend(loc='upper left')
    ax.set_xlabel('Daty')
    ax.set_ylabel('Kurs w PLN')
    ax.set_xlim(xmin=min(dates), xmax=max(dates))
    ax.set_ylim(ymin=3.6*1.1, ymax=4.9*1.1)
    plt.gcf().autofmt_xdate(rotation=25)
    fig.tight_layout()
    plt.show()
