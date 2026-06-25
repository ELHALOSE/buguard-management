from sqlalchemy.ext.asyncio import AsyncSession

from src.model import AssetRepository
from src.model.db_schema.darkatlas.schema.asset import Asset
from src.routes.schema.asset import AssetImportSchema

class AssetService:
    @staticmethod
    async def upsert_asset(db: AsyncSession, payload: AssetImportSchema):
        # تحويل البيانات إلى قاموس (Dict) ليتوافق مع SQLAlchemy
        payload_dict = {
            "id": payload.id,
            "type": payload.type,
            "value": payload.value,
            "status": "ACTIVE" if payload.status.lower() == "stale" else payload.status.upper(), # Handle re-appearing assets
            "source": payload.source,
            "tags": payload.tags,
            "metadata_json": payload.metadata
        }
        
        # استدعاء دالة الـ Upsert التي تمنع التكرار
        return await AssetRepository.upsert(db, payload_dict)

    @staticmethod
    async def get_all_assets(db: AsyncSession):
        return await AssetRepository.get_all(db)

    @staticmethod
    async def get_by_id_asset(db: AsyncSession,asset_id: str):
        return await AssetRepository.get_by_id(
            db,
            asset_id
        )

