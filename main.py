from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app import crud, database, schemas

app = FastAPI()


@app.on_event("startup")
def create_tables_sync():
    database.Base.metadata.create_all(bind=database.sync_engine)


def get_sync_db():
    db = database.SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db():
    async with database.AsyncSessionLocal() as session:
        yield session


@app.get("/")
def staring_project():
    return {"message": "Project starting successfully"}


@app.post("/users/sync", response_model=schemas.UserOut)
def create_user_sync(user: schemas.UserCreate, db: Annotated[Session, Depends(get_sync_db)]):
    return crud.create_user_sync(db, user)


@app.get("/users/sync", response_model=list[schemas.UserOut])
def get_users_sync(db: Annotated[Session, Depends(get_sync_db)]) -> list[schemas.UserOut]:
    return crud.get_users_sync(db)


@app.post("/users/async", response_model=schemas.UserOut)
async def create_user_async(
    user: schemas.UserCreate, db: Annotated[AsyncSession, Depends(get_async_db)]
) -> list[schemas.UserOut]:
    return await crud.create_user_async(db, user)


@app.get("/users/async", response_model=list[schemas.UserOut])
async def get_users_async(
    db: Annotated[AsyncSession, Depends(get_async_db)],
) -> list[schemas.UserOut]:
    return await crud.get_users_async(db)


def main() -> str:
    return "Hello From this project"
