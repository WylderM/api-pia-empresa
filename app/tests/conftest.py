import asyncio
import pytest
import pytest_asyncio
import os
from app.core.db import get_engine
from app.core.db_base import Base
from unittest.mock import patch, MagicMock, AsyncMock

os.environ["PYTEST_RUNNING"] = "1"

@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

class MockRedis:
    def __init__(self):
        self.data = {}
    
    async def get(self, key):
        return self.data.get(key)
    
    async def set(self, key, value, ex=None):
        self.data[key] = value
        return True

@pytest.fixture(autouse=True)
def mock_redis():
    mock_redis_client = MockRedis()
    
    def mock_make_cache_key(prefix, **kwargs):
        key_parts = [f"{k}:{v}" for k, v in sorted(kwargs.items()) if v is not None]
        return f"{prefix}:" + "|".join(key_parts)
    
    async def mock_get_cache(key):
        return None
    
    async def mock_set_cache(key, value, expire=300):
        return True
    
    with patch('app.core.cache.redis_client', mock_redis_client):
        with patch('app.core.cache.make_cache_key', mock_make_cache_key):
            with patch('app.core.cache.get_cache', mock_get_cache):
                with patch('app.core.cache.set_cache', mock_set_cache):
                    yield

@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_test_database():
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    
@pytest_asyncio.fixture(autouse=True)
async def db_session():
    engine = get_engine()
    connection = await engine.connect()
    transaction = await connection.begin()
    
    yield
    
    await transaction.rollback()
    await connection.close()