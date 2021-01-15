mess = """
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
    <title>{}</title>
    <h1>{}</h1>
    <p>{}</p>
    """


class ApiException(Exception):
    pass


class NoDataFound(ApiException):
    title = "Not found"
    status_code = 404

    def __init__(self, message, payload=None):
        Exception.__init__(self)
        self.message = '{}: {}'.format(self.status_code, message)
        self.payload = payload

    def to_dict(self):
        return mess.format(self.title, self.title, self.message)


class BadRequest(ApiException):
    title = "Bad request"
    status_code = 400

    def __init__(self, payload=None):
        Exception.__init__(self)
        self.message = 'Invalid request'
        self.payload = payload

    def to_dict(self):
        return mess.format(self.title, self.title, self.message)
