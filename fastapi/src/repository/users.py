from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.entity.models import User
from src.schemas.user import UserSchema


async def get_user_by_email(email: str, db: AsyncSession):
    try:
        stmt = select(User).filter_by(email=email)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        return user
    except Exception as e:
        print(f"Error in get_user_by_email: {e}")
        raise


async def create_user(body: UserSchema, db: AsyncSession):
    avatar = None
    try:
        new_user = User(**body.dict())
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except Exception as e:
        print(f"Error in create_user: {e}")
        raise


async def update_token(user: User, token: str | None, db: AsyncSession):
    user.refresh_token = token
    await db.commit()


async def confirmed_email(email: str, db: AsyncSession) -> None:
    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()


async def update_avatar(email, url: str, db: AsyncSession) -> User:
    user = await get_user_by_email(email, db)
    user.avatar = url
    await db.commit()
    await db.refresh(user)
    return user
