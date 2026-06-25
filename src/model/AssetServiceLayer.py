from sqlalchemy.ext.asyncio import AsyncSession

from src.model import AssetRepository
from src.model.db_schema.darkatlas.schema.asset import Asset


class AssetService:

    @staticmethod
    async def create_asset(db: AsyncSession,payload):
        asset = Asset(
            type=payload.type,
            value=payload.value,
            status=payload.status,
            source=payload.source,
            tags=payload.tags,
            metadata_json=payload.metadata_json
        )

        return await AssetRepository.create(
            db,
            asset
        )

    @staticmethod
    async def get_all_assets(db: AsyncSession):
        return await AssetRepository.get_all(db)

    @staticmethod
    async def get_by_id_asset(db: AsyncSession,asset_id: str):
        return await AssetRepository.get_by_id(
            db,
            asset_id
        )

