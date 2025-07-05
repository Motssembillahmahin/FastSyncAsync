from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

sync_engine = create_engine(settings.sync_database_url, echo=settings.debug)
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

async_engine = create_async_engine(settings.async_database_url, echo=settings.debug)
AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()
