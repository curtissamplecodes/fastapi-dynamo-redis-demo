from botocore.client import BaseClient
from fastapi import Depends, Request
from redis import Redis

from app.config import Settings
from app.users.handlers.create_user import CreateUserHandler
from app.users.handlers.get_user_by_id import GetUserByIdHandler


def get_settings(request: Request) -> Settings:
    return request.app.state.settings

def _get_dynamodb_client(request: Request) -> BaseClient:
    return request.app.state.dynamo

def _get_redis_client(request: Request) -> Redis:
    return request.app.state.redis

def get_create_user_handler(settings: Settings = Depends(get_settings),
                            dynamodb_client: BaseClient = Depends(_get_dynamodb_client)
) -> CreateUserHandler:
    return CreateUserHandler(settings, dynamodb_client)

def get_get_user_by_id_handler(settings: Settings = Depends(get_settings),
                               dynamodb_client: BaseClient = Depends(_get_dynamodb_client),
                               redis_client: Redis = Depends(_get_redis_client)
) -> GetUserByIdHandler:
    return GetUserByIdHandler(settings, dynamodb_client, redis_client)