from botocore.client import BaseClient
from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends, HTTPException, status
from redis.asyncio import Redis

from app.auth import verify_api_key
from app.config import Settings
from app.dependencies import get_dynamodb_client, get_redis_client, get_settings
from app.logging import logger, timing_logger
from app.users.handlers.create_user import CreateUserHandler
from app.users.handlers.get_user_by_id import GetUserByIdHandler
from app.users.models import User
from app.users.schemas import CreateUserRequest, CreateUserResponse
from app.utils.id_generator import generate_id

router = APIRouter(prefix="/users", tags=["users"], dependencies=[Depends(verify_api_key)])


@router.get("/{user_id}", response_model=User)
@timing_logger("get_user_by_id")
async def get_user_by_id(user_id: str, 
                         dynamodb_client: BaseClient = Depends(get_dynamodb_client),
                         redis_client: Redis = Depends(get_redis_client),
                         settings: Settings = Depends(get_settings)) -> User:
    handler = GetUserByIdHandler(settings, dynamodb_client, redis_client)

    try:
        if not (user := await handler.get(user_id)):
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except ClientError as ce:
        logger.error(f"DynamoDB client error: {ce.response['Error']['Message']}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to get user") from ce
    
@router.post("", status_code=status.HTTP_201_CREATED, response_model=CreateUserResponse)
@timing_logger("create_user")
async def create_user(user_request: CreateUserRequest, 
                      client: BaseClient = Depends(get_dynamodb_client),
                      settings: Settings = Depends(get_settings)) -> CreateUserResponse:    
    user = User(id=generate_id("usr"), name=user_request.name, date_of_birth=user_request.date_of_birth)
    handler = CreateUserHandler(settings, client)
    
    try:
        handler.create(user)
        return CreateUserResponse(id=user.id)
    except ClientError as ce:
        logger.error(f"DynamoDB client error: {ce.response['Error']['Message']}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to create user") from ce