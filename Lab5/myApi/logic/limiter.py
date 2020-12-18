from time import time as current_time
from logic.DataAPI.constants import MAX_REQ_PER_MINUTE, MINUTE_IN_SEC

class StaticVariables():
    requests = 0
    last_reset = current_time()

def can_request():
    if current_time() - StaticVariables.last_reset > MINUTE_IN_SEC:
        StaticVariables.requests = 0
        StaticVariables.last_reset = current_time()
    if StaticVariables.requests < MAX_REQ_PER_MINUTE:
        StaticVariables.requests += 1
        return True
    return False
