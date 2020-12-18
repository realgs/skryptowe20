# REST with Django Rest Framewok

---

This API offers simple GET request, fetching currency values to Polish Zloty. It also allows to get sale statistics based date parameter.
GET requests return in form of JSON.

1. [Install Guide](#install-guide)
1. [Adding new currency](#adding-new-currency)
1. [API usage](#api-usage)
1. [Limits](#limits)
1. [Dependencies](#dependencies)
1. [Credits](#credits)

---

## Install Guide
This projects implements automatic database creation for currency values. It also provides sample database file *sales.db* for sales statistic API demonstration.

1. **Clone this repo:**   
```git clone https://github.com/Rochala/skryptowe20.git ```
1. ** Checkout to REST branch **  
``` git checkout REST ```
1. **Install requirement**  
``` pip install -r requirements.txt ```
1. **Run initializing script**  
``` python3 init.py ```
1. **[OPTIONAL] Make sure models.py SalesStats contains every currency**  
1. ** Configure Django project to your needs **  
1. **Start django**  
``` python3 manage.py runserver ```

---

## Adding new currency
1. **Make sure NBP api supports it**  
1. **Add new currency symbol to constants.py Currency enum**  
1. **Run init.py script**  
```python3 init.py```
1. **Add new variable in models.py to SalesStats class following way:**  
```{CURRENCY_SYMBOL_LOWERCASED} = models.FloatField()```

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
Avaliable currencies are: 'USD', 'EUR', 'CHF'

---

## Dependencies
* [Django](https://www.djangoproject.com/)
* [Django REST Framework](https://www.django-rest-framework.org/)
* [requests](https://github.com/psf/requests)

---

## Credits
* [NBP](https://api.nbp.pl/en.html) for sharing currency API 
* [Kaggle](https://www.kaggle.com/kyanyoga/sample-sales-data/?select=sales_data_sample.csv) for sharing database sample data
