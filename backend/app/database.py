from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./stock.db")

async def get_db():
    async with async_session_maker() as session:
        yield session

engine = create_async_engine(DATABASE_URL, echo=True)

async_session_maker = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

class Base(DeclarativeBase):
    pass

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)