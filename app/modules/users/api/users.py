from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.modules.auth.schemas.user import UserOut, UserCreate
from app.modules.auth.services.auth import get_current_user
from app.modules.users.services import users as user_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=list[UserOut])
async def list_users(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await user_service.get_all_users(db)

@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    user = await user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user_in: UserCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    updated = await user_service.update_user(db, user_id, user_in.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    deleted = await user_service.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return None
