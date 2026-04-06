from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.repositories.user_repository import SQLAlchemyUserRepository
from app.services.user_service import UserService


def get_user_repository(db: AsyncSession = Depends(get_session)) -> SQLAlchemyUserRepository:
    return SQLAlchemyUserRepository(db)


def get_user_service(
    repository: SQLAlchemyUserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(repository)
