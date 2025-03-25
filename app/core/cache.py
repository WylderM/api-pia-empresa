import redis.asyncio as redis
import json
from hashlib import sha256
from app.core.config import settings

redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)

async def make_cache_key(path: str, params: dict):
    filtered = {k: v for k, v in params.items() if v is not None}
    raw_key = f"{path}:{json.dumps(filtered, sort_keys=True)}"
    return sha256(raw_key.encode()).hexdigest()

async def get_cache(key: str):
    return await redis_client.get(key)

async def set_cache(key: str, value: list, ttl: int = 300):
    await redis_client.set(key, json.dumps(value), ex=ttl)
