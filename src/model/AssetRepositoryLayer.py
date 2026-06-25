from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.model.db_schema.darkatlas.schema.asset import Asset
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from src.model.db_schema.darkatlas.schema.asset import Asset

class AssetRepository:

    @staticmethod
    async def upsert(db: AsyncSession, payload_dict: dict):
        #1. insert data into the database, if the id already exists, update the existing record
        stmt = insert(Asset).values(**payload_dict)
        
        # 2. If the record already exists, update the existing record with the new data
        do_update_stmt = stmt.on_conflict_do_update(
            index_elements=['id'],  # نفترض أن id هو المعرف الأساسي
            set_={
                'last_seen': func.now(),
                # دمج الـ tags القديمة مع الجديدة وإزالة التكرار
                'tags': func.array_cat(Asset.tags, stmt.excluded.tags),
                # دمج الـ metadata القديمة مع الجديدة (يفضل استخدام JSONB في الموديل)
                'metadata_json': Asset.metadata_json.op('||')(stmt.excluded.metadata_json),
                'status': stmt.excluded.status, # تحديث الحالة ربما عاد نشطاً
            }
        )
        
        await db.execute(do_update_stmt)
        await db.commit()

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

