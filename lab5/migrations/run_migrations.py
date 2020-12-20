import os
from database.connection import connect
from database.commands import insert_into_pln_currencies, currencies_table_empty
from nbp_requests import get_currency_for_period, fill_empty_records, MIN_ALLOWED_DATE, MAX_ALLOWED_DATE

def run_scripts():
    scripts_path = "sql_scripts/"

    print("\nConnecting to the DB...")

    with connect() as conn:
        cursor = conn.cursor()

        print("\nRunning Scripts...")

        script_paths = os.listdir(scripts_path)
        init_script = script_paths[0]
        add_sales_table_script = script_paths[1]

        with open(f"{scripts_path}/{init_script}", "r") as script_file:
            script = script_file.read()
            script_file.close()
            cursor.execute(script)

        if currencies_table_empty():
            insert_interpolated_currencies()

        with open(f"{scripts_path}/{add_sales_table_script}", "r") as script_file:
            script = script_file.read()
            script_file.close()
            cursor.execute(script)

        conn.commit()
        print("\nChanges successfully committed")
        print("\nClosing DB...")


def insert_interpolated_currencies():
    start_date = MIN_ALLOWED_DATE
    end_date = MAX_ALLOWED_DATE

    currencies_for_period = get_currency_for_period("USD", start_date, end_date)
    fixed_currencies = fill_empty_records(currencies_for_period, start_date, end_date)

    for currency in fixed_currencies:
        insert_into_pln_currencies(currency)


if __name__ == "__main__":
    run_scripts()