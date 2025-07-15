from asyncio import to_thread

from botocore.exceptions import ClientError
from redis.exceptions import RedisError

from app.logging import logger
from app.users.handlers.base_handler import BaseHandler
from app.users.models import User
from app.utils.cache_keys import redis_cache_key


class GetUserByIdHandler(BaseHandler):
    async def get(self, user_id: str) -> User | None:
        redis_key = redis_cache_key("user", user_id)

        if user := await self._try_redis(user_id, redis_key):
            return user
        
        return await self._fallback_to_dynamo_and_cache(user_id, redis_key)
        
    async def _try_redis(self, user_id: str, key: str) -> User | None:
        try:
            if cached := await self.redis_client.get(key):
                logger.info("user.cache.hit", extra={"user_id": user_id})
                return User.from_redis(cached)
            
            logger.info("user.cache.miss", extra={"user_id": user_id})
        except RedisError:
            logger.warning("user.redis.error", extra={"user_id": user_id}, exc_info=True)

        return None
    
    async def _fallback_to_dynamo_and_cache(self, user_id: str, redis_key: str) -> User | None:
        try:
            response = await to_thread(self.dynamodb_client.get_item,
                TableName=self.settings.USERS_TABLE_NAME,
                Key={"id": {"S": user_id}}
            )

            if not (item := response.get("Item")):
                logger.warning(f"User not found {user_id}")
                return None

            user = User.from_dynamo(item)
            await self._cache_to_redis(user, redis_key)
            return user
        except ClientError as ce:
            logger.error("user.dynamo.error", extra={"user_id": user_id}, exc_info=True)
            raise RuntimeError(f"DynamoDB error: {ce.response['Error']['Message']}") from ce

    async def _cache_to_redis(self, user: User, key: str) -> None:
        try:
            await self.redis_client.set(key, user.to_redis(), ex=self.settings.USER_CACHE_TTL_SECONDS)
        except RedisError:
            logger.warning("user.redis.error", extra={"user_id": user.id}, exc_info=True)