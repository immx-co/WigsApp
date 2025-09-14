import os

from schemas.base import Base
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

PG_USER = os.getenv("PG_USER", "postgres")
PG_PASSWORD = os.getenv("PG_PASSWORD", "")
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = int(os.getenv("PG_PORT", "5432"))
ADMIN_DB = os.getenv("PG_ADMIN_DB", "postgres")
APP_DB = os.getenv("PG_APP_DB", "some_db")

ADMIN_URL = (
    f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{ADMIN_DB}"
)
APP_URL = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{APP_DB}"

engine = create_async_engine(APP_URL, echo=False, pool_pre_ping=True)
async_session_maker = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def init_db() -> None:
    admin_engine = create_async_engine(ADMIN_URL, echo=False, pool_pre_ping=True)

    # 1) Проверяем, существует ли БД (отдельное соединение, без AUTOCOMMIT)
    async with admin_engine.connect() as conn:
        res = await conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :name"),
            {"name": APP_DB},
        )
        exists = res.scalar() is not None

    # 2) Если нет — открываем НОВОЕ соединение с AUTOCOMMIT и создаём БД
    if not exists:
        autocommit_engine = admin_engine.execution_options(isolation_level="AUTOCOMMIT")
        async with autocommit_engine.connect() as conn:
            await conn.exec_driver_sql(f'CREATE DATABASE "{APP_DB}"')

    await admin_engine.dispose()

    # 3) Создаём таблицы уже в целевой БД
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# зависимость для FastAPI
async def get_db():
    async with async_session_maker() as session:
        yield session
        yield session
