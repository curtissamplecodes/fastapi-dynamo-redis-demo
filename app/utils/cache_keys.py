def redis_cache_key(prefix: str, identifier: str) -> str:
    return f"{prefix}:{identifier}"