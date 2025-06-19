import pytest

from app.utils.cache_keys import redis_cache_key


@pytest.mark.parametrize(
    "prefix, identifier, expected",
    [
        ("user", "123", "user:123"),
        ("session", "abc", "session:abc")
    ]
)
def test_redis_key(prefix: str, identifier: str, expected: str) -> None:
    assert redis_cache_key(prefix, identifier) == expected