from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService
from app.dependencies import get_user_service

router = APIRouter()


@router.post("", response_model=UserRead)
async def create_user(
    user_in: UserCreate,
    service: UserService = Depends(get_user_service),
):
    try:
        return await service.create_user(user_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    user = await service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
