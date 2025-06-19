from botocore.client import BaseClient
from redis.asyncio import Redis

from app.config import Settings


class BaseHandler:
    def __init__(self, settings: Settings, dynamodb_client: BaseClient, redis_client: Redis | None = None):
        self.settings = settings
        self.dynamodb_client = dynamodb_client
        self.redis_client = redis_client