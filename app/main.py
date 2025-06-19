from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.clients import configure_logging, create_dynamodb_client, create_redis_client
from app.config import Settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings().with_secrets()
    app.state.settings = settings
    app.state.dynamo = create_dynamodb_client(settings)

    redis = create_redis_client(settings)
    app.state.redis = redis
    configure_logging(settings)
    yield
    await redis.aclose()

def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    
    # Import after app is initialized to ensure decorators and dependencies are safe
    from app.users import api  # noqa: E402
    app.include_router(api.router)

    return app

app = create_app()