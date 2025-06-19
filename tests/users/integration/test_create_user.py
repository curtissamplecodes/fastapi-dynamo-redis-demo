import re

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.integration
async def test_create_user(test_client: AsyncClient):
    name = "Curtis Sample"
    dob = "1981-11-24"
    payload = {
        "name": name,
        "date_of_birth": dob
    }
     
    post_response = await test_client.post("/users", json=payload)
    
    assert post_response.status_code == 201

    user_id = post_response.json()["id"]
    assert re.match(r"^usr_[a-z0-9_-]{22}$", user_id)

    expected_user = {
        "id": user_id,
        "name": name,
        "date_of_birth": dob
    }

    get_response = await test_client.get(f"/users/{user_id}")

    assert get_response.status_code == 200
    assert get_response.json() == expected_user