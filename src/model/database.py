#نفس الفايل darkatlas_base.py

# src/model/database.py

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)

from sqlalchemy.orm import sessionmaker

from src.helper.config import get_settings


settings = get_settings()

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session