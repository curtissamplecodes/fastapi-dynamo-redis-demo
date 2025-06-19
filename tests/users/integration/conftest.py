from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from botocore.client import BaseClient
from httpx import ASGITransport, AsyncClient
from redis.asyncio import Redis

from app.main import app


@pytest_asyncio.fixture
async def test_client() -> AsyncGenerator[AsyncClient, None]:
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        headers = {"x-api-key": app.state.settings.API_KEY}
        async with AsyncClient(transport=transport, base_url="http://test", headers=headers) as client:
            yield client

@pytest.fixture(scope="module")
def dynamodb_client() -> Generator[BaseClient, None, None]:
    return app.state.dynamo

@pytest.fixture(scope="module")
def redis_client() -> Redis:
    return app.state.redis