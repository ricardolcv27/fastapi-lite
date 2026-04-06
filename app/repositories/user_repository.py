from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate
from app.repositories.interfaces.user_repository import IUserRepository


class SQLAlchemyUserRepository(IUserRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def create(self, user_in: UserCreate) -> User:
        user = User(email=user_in.email, full_name=user_in.full_name)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
