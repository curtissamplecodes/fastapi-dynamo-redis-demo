from dataclasses import dataclass

from app.users.models import User


@dataclass
class GetUserResult:
    user: User
    is_cache_hit: bool = False

    @property
    def cache_hit_header(self) -> str:
        return "true" if self.is_cache_hit else "false"