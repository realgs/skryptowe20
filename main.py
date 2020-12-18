import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import cache
import api
from constans import CACHE_UPDATE_INTERVAL

if __name__ == "__main__":
    cache.update_cache()
    refresh = BackgroundScheduler()
    refresh.add_job(cache.update_cache, 'interval', hours=CACHE_UPDATE_INTERVAL, replace_existing=True)
    refresh.start()
    atexit.register(lambda: refresh.shutdown(wait=False))

    api.run()
