from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.modules.auth.models.user import User
from app.modules.auth.schemas.user import UserCreate
from app.modules.auth.services.auth import get_password_hash

async def get_all_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()

async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def update_user(db: AsyncSession, user_id: int, user_data: dict):
    user = await get_user_by_id(db, user_id)
    if not user:
        return None
    for field, value in user_data.items():
        if field == "password":
            setattr(user, "hashed_password", get_password_hash(value))
        elif hasattr(user, field):
            setattr(user, field, value)
    await db.commit()
    await db.refresh(user)
    return user

async def delete_user(db: AsyncSession, user_id: int):
    user = await get_user_by_id(db, user_id)
    if not user:
        return None
    await db.delete(user)
    await db.commit()
    return True
