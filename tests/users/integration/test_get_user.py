import pytest
from botocore.client import BaseClient
from httpx import AsyncClient
from redis import Redis

from app.config import Settings
from app.utils.cache_keys import redis_cache_key
from app.utils.id_generator import generate_id

settings = Settings()


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_user_by_id(test_client: AsyncClient, dynamodb_client: BaseClient):
    user_id = generate_id("usr")
    _seed_user(dynamodb_client, user_id)

    try:
        expected_user = {
            "id": user_id,
            "name": "Curtis Sample",
            "date_of_birth": "1987-06-04"
        }
         
        response = await test_client.get(f"/users/{user_id}")
        
        assert response.status_code == 200
        assert response.json() == expected_user
    finally:
        await _clear_user(user_id, dynamodb_client)

@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_user_by_id_not_found(test_client: AsyncClient):
    response = await test_client.get("/users/999")
    assert response.status_code == 404

@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_user_by_id_cache_aside(test_client: AsyncClient, dynamodb_client: BaseClient, redis_client: Redis) -> None:
    user_id = generate_id("usr")
    _seed_user(dynamodb_client, user_id)
    redis_key = redis_cache_key("user", user_id)

    try:
        await redis_client.delete(redis_key)

        # comes from Dynamo
        first_response = await test_client.get(f"/users/{user_id}")
        assert first_response.status_code == 200

        cached = await redis_client.get(redis_key)
        assert cached is not None

        # comes from Redis
        second_response = await test_client.get(f"/users/{user_id}")
        assert second_response.status_code == 200
        assert second_response.json() == first_response.json()
    finally:
        await _clear_user(user_id, dynamodb_client, redis_client)

def _seed_user(dynamodb_client, user_id: str, name: str = "Curtis Sample", dob: str = "1987-06-04") -> None:
    response = dynamodb_client.put_item(
        TableName=settings.USERS_TABLE_NAME,
        Item={
            "id": {"S": user_id},
            "name": {"S": name},
            "date_of_birth": {"S": dob},
        }
    )

    status_code = response["ResponseMetadata"]["HTTPStatusCode"]
    assert status_code == 200, f"Put item failed with status code {status_code}"

async def _clear_user(user_id: str,
                      dynamodb_client: BaseClient, 
                      redis_client: Redis | None = None) -> None:
    if redis_client is not None:
        await redis_client.delete(user_id)

    dynamodb_client.delete_item(
        TableName=settings.USERS_TABLE_NAME,
        Key={"id": {"S": user_id}},
    )