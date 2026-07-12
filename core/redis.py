from django.conf import settings

import redis

def check_redis():

    try:

        client = redis.Redis.from_url(settings.REDIS_URL)

        client.ping()

        print("Redis Connected")

        return True

    except Exception as e:

        print("Redis Error:", e)

        return False