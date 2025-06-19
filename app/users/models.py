from datetime import date

from pydantic import BaseModel


class User(BaseModel):
    id: str
    name: str
    date_of_birth: date

    @classmethod
    def from_dynamo(cls, item: dict) -> "User":
        return cls(
            id=item["id"]["S"],
            name=item["name"]["S"],
            date_of_birth=date.fromisoformat(item["date_of_birth"]["S"])
        )
    
    def to_dynamo(self) -> dict:
        return {
            "id": {"S": self.id},
            "name": {"S": self.name},
            "date_of_birth": {"S": self.date_of_birth.isoformat()},
        }
    
    @classmethod
    def from_redis(cls, json: str) -> "User":
        return cls.model_validate_json(json)
    
    def to_redis(self) -> str:
        return self.model_dump_json()