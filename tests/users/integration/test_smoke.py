import pytest
from botocore.client import BaseClient
from redis.asyncio import Redis

from app.config import Settings

settings = Settings()

@pytest.mark.smoke
def test_smoke_dynamo_table_exists(dynamodb_client: BaseClient) -> None:
    tables = dynamodb_client.list_tables()["TableNames"]
    assert settings.USERS_TABLE_NAME in tables, f"Expected value {settings.USERS_TABLE_NAME} not found in tables"

@pytest.mark.asyncio
@pytest.mark.smoke
async def test_redis_up(redis_client: Redis) -> None:
    assert await redis_client.ping(), "Redis PING did not respond"
    await redis_client.set("smoke:test", "ok", ex=5)
    assert await redis_client.get("smoke:test") == "ok", "Redis GET returned unexpected result"