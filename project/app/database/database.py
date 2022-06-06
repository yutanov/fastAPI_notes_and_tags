import os

from sqlmodel import SQLModel

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


DATABASE_DEFAULT_URL = "postgresql+asyncpg://postgres:postgres@db:5432/notes_API"
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL is None:
    print("[Database Error] Environment Parameter - DATABASE_URL is None")
    print(f"[Database Error] I Use The Default Value: {DATABASE_DEFAULT_URL}")
    DATABASE_URL = DATABASE_DEFAULT_URL

engine = create_async_engine(DATABASE_URL, echo=True, future=True)


async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
