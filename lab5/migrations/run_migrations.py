import os
from database.connection import connect
from database.commands import insert_into_pln_currencies
from nbp_requests import get_currency_for_period, fill_empty_records
from datetime import date

def run_scripts():
    scripts_path = "sql_scripts/"

    print("\nConnecting to the DB...")
    conn = connect()

    with conn:
        cursor = conn.cursor()

        print("\nReading Scripts...")
        for script_path in os.listdir(scripts_path):
            script_file = open(f"{scripts_path}/{script_path}", "r")
            script = script_file.read()
            script_file.close()

            print(f"Executing Script {script_path} ...")
            cursor.execute(script)

        conn.commit()
        print("\nChanges successfully committed")
        print("\nClosing DB...")


def insert_interpolated_currencies():
    # Min and max ranges from DB. TODO get range using SQL query
    start_date = date(2003, 10, 26)
    end_date = date(2004, 8, 24)

    currencies_for_period = get_currency_for_period("USD", start_date, end_date)
    fixed_currencies = fill_empty_records(currencies_for_period, start_date, end_date)

    for currency in fixed_currencies:
        insert_into_pln_currencies(currency)


if __name__ == "__main__":
    run_scripts()
    insert_interpolated_currencies()