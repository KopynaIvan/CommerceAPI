import json
import redis
import os

redis_client = redis.from_url(os.environ.get("REDIS_URL", "redis://redis:6379/0"))

def get_cached(key: str):
    data = redis_client.get(key)
    if data:
        return json.loads(data.decode("utf-8"))
    return None

def set_cached(key: str, value, expiry: int = 60):
    redis_client.set(key, json.dumps(value), ex=expiry)

def invalidate_cache(key: str):
    redis_client.delete(key)
