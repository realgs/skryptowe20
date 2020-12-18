# REST with Django Rest Framewok
This API offers simple GET request, fetching currency values to Polish Zloty. It also allows to get sale statistics based date parameter.
GET requests return in form of JSON.

1. [Install Guide](#install-guide)
1. [API usage](#api-usage)
1. [Limits](#limits)
1. [Dependencies](#dependencies)
---

## Install Guide
This projects implements automatic database creation for currency values. To make sale statistics to work you will need to make some changes to the code and provide your own database with sales.

**Clone this repo:**
```git clone https://github.com/Rochala/skryptowe20.git ```
** Checkout to REST branch **
``` git checkout REST ```
** Run script **
``` python3 fetch_currency.py ```
** Configure Django project to your needs **
**Start django**
``` python3 manage.py runserver ```

---
## API usage
**Currency data range**
``` http://127.0.0.1:8000/CurrencyRange/?symbol={CURRENCY SYMBOL}start={DATE START}&end={DATE END} ```
*Example usage for USD between 2020-12-01 and 2020-12-16*
``` http://127.0.0.1:8000/CurrencyRange/?symbol=USD&start=2020-12-01&end=2020-12-16 ```

**Sales statistics**
```http://127.0.0.1:8000/SaleStats/?date={SELECTED DATE}```
*Example usage for fetching sales from 2005-05-17*
```http://127.0.0.1:8000/SaleStats/?date=2005-05-17 ```
*You can also get whole range by using*
```http://127.0.0.1:8000/SaleStats/```

---
## Limits
|User type | Limit |
|:-|:-
| Anonymous user: | 10 / hour |
|Standard User : | 1000 / hour |

Currency API is also limited by dates **2001-01-02** and **2020-12-17**  
Avaliable currencies are: 'USD', 'EUR'

---

## Dependencies
* [Django](https://www.djangoproject.com/)
* [Django REST Framework](https://www.django-rest-framework.org/)
* [requests](https://github.com/psf/requests)
