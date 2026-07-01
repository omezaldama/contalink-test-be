import redis

from app.config import settings


cache = redis.Redis(settings.redis_host, settings.redis_port)


class CacheService:
    def set(self, key: str, val: str) -> None:
        try:
            cache.set(key, val, ex=60*settings.redis_ttl_mins)
        except Exception as e:
            print(f'Cache set error: {e}')

    def get(self, key: str) -> str | None:
        try:
            return cache.get(key)
        except Exception as e:
            print(f'Cache get error: {e}')
