from app.models.user import User
from app.schemas.user import UserCreate
from app.repositories.interfaces.user_repository import IUserRepository


class UserService:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    async def create_user(self, user_in: UserCreate) -> User:
        existing = await self.repository.get_by_email(user_in.email)
        if existing:
            raise ValueError("Email already registered")
        return await self.repository.create(user_in)

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.repository.get_by_id(user_id)
