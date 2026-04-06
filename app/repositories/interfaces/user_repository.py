from abc import ABC, abstractmethod
from app.models.user import User
from app.schemas.user import UserCreate


class IUserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def create(self, user_in: UserCreate) -> User: ...
