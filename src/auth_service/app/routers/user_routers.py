from fastapi import APIRouter, Depends

from src.auth_service.app.dependencies import (
    get_user_service,
    verify_service_credentials,
)
from src.auth_service.app.services import AsyncUserService
from src.auth_service.app.schemas import UserResponseSchema

router = APIRouter()


@router.get("/{user_id}")
async def get_user_by_id(
    user_id: int,
    _auth: None = Depends(verify_service_credentials),
    user_service: AsyncUserService = Depends(get_user_service),
) -> UserResponseSchema:
    user = await user_service.get_by_id(user_id)
    return UserResponseSchema.model_validate(user)
