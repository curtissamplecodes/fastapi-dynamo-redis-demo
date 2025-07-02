from asyncio import to_thread
from botocore.exceptions import ClientError

from app.users.handlers.base_handler import BaseHandler
from app.users.models import User


class CreateUserHandler(BaseHandler):
    async def create(self, user: User) -> None:
        try:
            await to_thread(self.dynamodb_client.put_item,
                TableName=self.settings.USERS_TABLE_NAME,
                Item=user.to_dynamo())
        except ClientError as ce:
            raise RuntimeError(f"DynamoDB error: {ce.response['Error']['Message']}") from ce