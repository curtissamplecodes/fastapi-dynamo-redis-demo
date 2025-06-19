from typing import Annotated

from fastapi import Depends, Header, HTTPException, status

from app.config import Settings
from app.dependencies import get_settings


async def verify_api_key(
        x_api_key: Annotated[str | None, Header()],
        settings: Settings = Depends(get_settings)) -> None:
    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API key")