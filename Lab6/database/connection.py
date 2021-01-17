import psycopg2
from .connection_params import ConnectionParams
from os import path

def connect():
    conn_params = _load_connection_params()
    try:
        conn = psycopg2.connect(user=conn_params.user,
                                password=conn_params.password,
                                host=conn_params.host,
                                port=conn_params.port,
                                database=conn_params.database)
        return conn
    except (Exception, psycopg2.Error) as ex:
        print("Error while connecting to PostgreSQL", ex)


def _load_connection_params():
    root_dir = path.dirname(path.abspath(__file__))
    try:
        with open(f"{root_dir}\ConnectionString.txt") as file:
            connection_params_list = list(map(lambda x: x[x.index("=") + 1:], file.read().split(',')))

            if len(connection_params_list) != 5:
                raise ValueError("`ConnectionString.txt` has wrong format, check .example template")

        return ConnectionParams(connection_params_list)

    except IOError:
        print("Error while reading from `ConnectionString.txt` file")
