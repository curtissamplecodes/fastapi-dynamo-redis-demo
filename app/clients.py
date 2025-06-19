import boto3
import seqlog
from botocore.client import BaseClient
from redis.asyncio import Redis

from app.config import Settings


def configure_logging(settings: Settings) -> None:
    seqlog.log_to_seq(
        server_url=settings.SEQ_URL,
        level="INFO",
        batch_size=1,
        auto_flush_timeout=1
    )

def create_dynamodb_client(settings: Settings) -> BaseClient:
    return boto3.client(
        "dynamodb",
        endpoint_url=settings.AWS_ENDPOINT,
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY,
        aws_secret_access_key=settings.AWS_SECRET_KEY
    )

def create_redis_client(settings: Settings) -> Redis:
    return Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        decode_responses=True
    )