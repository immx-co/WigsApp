# engine.py
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncAttrs,
)
from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy import Column, String, Integer, text


PG_USER = "postgres"
PG_PASSWORD = "123"
PG_HOST = "localhost"
PG_PORT = 5433
ADMIN_DB = "postgres"
APP_DB = "antoshadb"

ADMIN_URL = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{ADMIN_DB}"
APP_URL   = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{APP_DB}"

engine = create_async_engine(APP_URL, echo=False, pool_pre_ping=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

class Person(Base):
    __tablename__ = "people"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)

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