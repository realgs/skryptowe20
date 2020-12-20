# Flask API
## Currency rates and sales - USD and PLN

## This API uses Northwind SQLite Database
https://github.com/jpwhite3/northwind-SQLite3

## USD and PLN rates are from http://api.nbp.pl/ API

# Prerequisites
1. Install packages by running ``` pip install -r requirements.txt ```.
2. Download the database from https://github.com/jpwhite3/northwind-SQLite3 and place all files into ``` /Source ``` folder.
<br>
Or change paths relative to the db folder in ``` src/conf.py ``` file and ``` src/database/db_startup.py ``` file.
3. Run scripts from ``` /Source ``` folder.
   ```
    $ sqlite3 bazunia.db < Northwind.Sqlite3.create.sql
    $ sqlite3 bazunia.db < Northwind.Sqlite3.update.sql
   ```
#### Optionally you can change configuration in ``` src/conf.py ``` file.

# Run the app
1. Run ``` src/database/db_startup.py ``` script to prepare database.
2. Run in terminal ``` set FLASK_APP=api.py ``` (in cmd).
  <br>
  And run in terminal ``` flask run ```.

# Endpoints
- ``` http://127.0.0.1:8080/api/rates ``` - to get all rates usd to pln

- ``` http://127.0.0.1:8080/api/rates/{date} ``` - to get rate usd to pln for the specified date.

- ``` http://127.0.0.1:8080/api/rates/{start_date}/{end_date} ``` - to get rate usd to pln for the specified range of dates.

- ``` http://127.0.0.1:8080/api/sales/{date} ``` - to get sales for the specified date.

- ``` http://127.0.0.1:8080/api/sales/{start_date}/{end_date} ``` - to get sales for the specified range of dates.

# Others
- Cache timeout is set to 50.
- Request limits are set to "200 per day" and "50 per hour".
