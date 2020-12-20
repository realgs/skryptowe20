class ConnectionParams:
    def __init__(self, connection_params_list: list):
        self.user = connection_params_list[0]
        self.password = connection_params_list[1]
        self.host = connection_params_list[2]
        self.port = connection_params_list[3]
        self.database = connection_params_list[4]