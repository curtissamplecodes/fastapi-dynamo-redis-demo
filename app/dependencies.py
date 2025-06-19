from botocore.client import BaseClient
from fastapi import Request
from redis import Redis

from app.config import Settings


def get_settings(request: Request) -> Settings:
    return request.app.state.settings

def get_dynamodb_client(request: Request) -> BaseClient:
    return request.app.state.dynamo

def get_redis_client(request: Request) -> Redis:
    return request.app.state.redis