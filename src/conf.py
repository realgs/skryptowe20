conf = {
  'db': {
    'db_name' : "../Source/bazunia.db"
  },
  'limits': ["200 per day", "50 per hour"],
  'cache': {'CACHE_TYPE': 'simple'},
  'api': {
    'host': '0.0.0.0',
    'port': 8080,
    'debug': True
  }
}


API_ERROR_NOT_FOUND = {'status': 404, 'info': "Data not found"}
API_ERROR_BAD_REQ = {'status': 400, 'info': "Bad request"}
API_ERROR_TOO_MANY_REQS = {'status': 429, 'info': "Too many requests"}
