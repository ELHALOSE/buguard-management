from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.model.db_schema.darkatlas.schema.asset import Asset


class AssetRepository:

    @staticmethod
    async def create(db: AsyncSession,asset: Asset):
        db.add(asset)

        await db.commit()
        await db.refresh(asset)

        return asset

    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(
            select(Asset)
        )

        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession,asset_id: str):
        result = await db.execute(
            select(Asset).where(
                Asset.id == asset_id
            )
        )

        return result.scalar_one_or_none()

