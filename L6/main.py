#!/usr/bin/python3

import sqlite3
import database
import currency_API

import api

DATABASE_NAME = "sales_data.db"

if __name__ == "__main__":

    # basic configuration
    if not database.table_exists("markings"):
        database.assure_markings()
        database_from = currency_API.string_to_datetime('2014-10-16')
        database_to = currency_API.string_to_datetime('2020-12-16')
        database.refill_markings('USD', database_from, database_to)

    print(database.get_available_currencies())
    api.run_app()
