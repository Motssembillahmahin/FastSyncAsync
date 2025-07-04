from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from . import models, schemas


def create_user_sync(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users_sync(db: Session) -> list[str]:
    return db.query(models.User).all()


async def create_user_async(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_users_async(db: AsyncSession):
    result = await db.execute(select(models.User))
    return result.scalars().all()
