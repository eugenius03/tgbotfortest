from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import URL, create_engine, text, insert

def get_url():
    return "sqlite+aiosqlite:///database.db"


async_engine = create_async_engine(
        url=get_url(),
        echo=False,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=3600,
)
async_session=async_sessionmaker(async_engine, expire_on_commit=False)

async def create_tables():
     async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

class Base(DeclarativeBase):
    pass
