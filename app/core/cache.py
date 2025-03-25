import aioredis
from app.core.config import settings
import json

redis_client = aioredis.from_url(settings.redis_url, decode_responses=True)


def make_cache_key(prefix: str, **kwargs) -> str:
    key_parts = [f"{k}:{v}" for k, v in sorted(kwargs.items())]
    key = f"{prefix}:" + "|".join(key_parts)
    return key


async def get_cache(key: str):
    cached_data = await redis_client.get(key)
    if cached_data:
        return json.loads(cached_data)
    return None


async def set_cache(key: str, value, expire: int = 300):
    await redis_client.set(key, json.dumps(value), ex=expire)
