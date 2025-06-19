from datetime import date

from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    name: str
    date_of_birth: date

class CreateUserResponse(BaseModel):
    id: str