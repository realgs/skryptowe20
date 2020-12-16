from db_handler import connect_to_db
rates = {}


def update_cache():
    conn = connect_to_db()
    c = conn.cursor()
    c.execute('''SELECT * FROM avg_rates''')
    rows = c.fetchall()
    for row in rows:
        rates[row[0]] = {'rate': row[1], 'interpolated': row[2]}
    conn.close()


update_cache()
