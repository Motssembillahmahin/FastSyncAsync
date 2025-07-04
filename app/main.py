from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app import crud, schemas

from .database import AsyncSessionLocal, Base, SyncSessionLocal, sync_engine

app = FastAPI()


@app.on_event("startup")
def create_tables_sync():
    Base.metadata.create_all(bind=sync_engine)


def get_sync_db():
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session


@app.post("/users/sync", response_model=schemas.UserOut)
def create_user_sync(user: schemas.UserCreate, db: Session = Depends(get_sync_db)):
    return crud.create_user_sync(db, user)


@app.get("/users/sync", response_model=list[schemas.UserOut])
def get_users_sync(db: Session = Depends(get_sync_db)):
    return crud.get_users_sync(db)


@app.post("/users/async", response_model=schemas.UserOut)
async def create_user_async(user: schemas.UserCreate, db: AsyncSession = Depends(get_async_db)):
    return await crud.create_user_async(db, user)


@app.get("/users/async", response_model=list[schemas.UserOut])
async def get_users_async(db: AsyncSession = Depends(get_async_db)):
    return await crud.get_users_async(db)
