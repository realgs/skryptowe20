<!--MAIN DESCRIPTION -->
## About The Project

This is very brief documentation about api that provides information about currency rates based on nbp api.

Main funcionalities:
* access to multiple currencies rates in a given time
* access to currencies rates in a given period of time
* minimalistic front end to present data

### Quick introduction

To get json rates use base path:
https://localhost:port/api/currency/{CurrencyCode}
Example:
https://localhost:port/api/currency/USD

In order to get rates for a certain day use:
https://localhost:port/api/currency/{CurrencyCode}/{StartDate}
Example:
https://localhost:port/api/currency/USD/2020-02-01

for a period of time:
https://localhost:port/api/currency/{CurrencyCode}/{StartDate}/{EndDate}
Example:
https://localhost:port/api/currency/USD/2020-02-01/2020-02-15

To see base front page with few example currencies use:
https://localhost:path/api

### Built With

* .NET Core (both front and back - api)

### Final thoughts

Not gonna lie, this project is not only delayed but also vastly underdeveloped, the main reason behind it is my lack of time in recent weeks