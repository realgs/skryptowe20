from .connection import connect

def insert_into_pln_currencies(currency):
    conn = connect()
    with conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO purchasing.pln_currencies(currency_date, currency_value, interpolated) VALUES(%s, %s, %s)", currency)

# def execute_custom_query(query: str):
#     conn = connect()
#     cursor = conn.cursor()
#     try:
#         cursor.execute(query)
#         query_result = cursor.fetchall()
#         return query_result
#     finally:
#         cursor.close()
#         conn.close()
