from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.modules.auth.schemas.user import UserCreate, UserOut, Token
from app.modules.auth.models.user import User
from app.modules.auth.services.auth import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_user,
)
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserOut)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    from sqlalchemy.future import select
    from sqlalchemy.exc import IntegrityError

    user_exists = await db.execute(select(User).where(User.email == user_in.email))
    if user_exists.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user_in.email,
        name=user_in.name,
        hashed_password=get_password_hash(user_in.password)
    )
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="User creation failed")

    return new_user

@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
