import json
from typing import Self

import boto3
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SEQ_URL: str
    AWS_ENDPOINT: str
    AWS_REGION: str
    AWS_ACCESS_KEY: str
    AWS_SECRET_KEY: str
    USERS_TABLE_NAME: str = "Users"
    REDIS_HOST: str
    REDIS_PORT: int
    USER_CACHE_TTL_SECONDS: int = 300
    API_KEY: str = "load-from-secrets"

    model_config = ConfigDict(env_file=".env")

    def with_secrets(self, secret_id: str = "api-key") -> Self:
        secrets = self._fetch_secrets(secret_id)
        self.API_KEY = secrets.get("key")
        return self
    
    def _fetch_secrets(self, secret_id: str) -> dict:
        client = boto3.client(
            "secretsmanager",
            endpoint_url=self.AWS_ENDPOINT,
            region_name=self.AWS_REGION,
            aws_access_key_id=self.AWS_ACCESS_KEY,
            aws_secret_access_key=self.AWS_SECRET_KEY
        )
        response = client.get_secret_value(SecretId=secret_id)
        return json.loads(response["SecretString"])