from sqlalchemy.ext.asyncio import AsyncSession

from src.model import AssetRepository
from src.model.db_schema.darkatlas.schema.asset import Asset
from src.routes.schema.asset import AssetImportSchema
from src.model.db_schema.darkatlas.schema.asset_relationship import AssetRelationship

class AssetService:
    @staticmethod
    async def upsert_asset(db: AsyncSession, payload: AssetImportSchema):
        # 1. تحويل البيانات (كما هي)
        payload_dict = {
            "id": payload.id,
            "type": payload.type,
            "value": payload.value,
            "status": "ACTIVE" if payload.status.lower() == "stale" else payload.status.upper(),
            "source": payload.source,
            "tags": payload.tags,
            "metadata_json": payload.metadata
        }
        
        await AssetRepository.upsert(db, payload_dict)
        
        # 2. تعديل منطق العلاقة ليكون آمناً
        if payload.parent and payload.parent != "string": 
            # التحقق هل الـ parent موجود فعلياً في قاعدة البيانات؟
            parent_asset = await AssetRepository.get_by_id(db, payload.parent)
            
            if parent_asset:
                # التحقق من عدم تكرار العلاقة
                stmt = select(AssetRelationship).where(...)
                result = await db.execute(stmt)
                if not result.scalar_one_or_none():
                    rel = AssetRelationship(
                        source_asset_id=payload.parent,
                        target_asset_id=payload.id,
                        relationship_type="parent_of"
                    )
                    db.add(rel)
                    await db.commit()
            else:
                # اختياري: يمكنك طباعة log هنا بأن الـ parent غير موجود
                print(f"Warning: Parent {payload.parent} not found, skipping relationship.")
            
        return {"status": "success", "id": payload.id}
    @staticmethod
    async def get_all_assets(db: AsyncSession):
        return await AssetRepository.get_all(db)

    @staticmethod
    async def get_by_id_asset(db: AsyncSession,asset_id: str):
        return await AssetRepository.get_by_id(
            db,
            asset_id
        )

