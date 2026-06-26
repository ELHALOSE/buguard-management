from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.model.db_schema.darkatlas.schema.asset import Asset
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from src.model.db_schema.darkatlas.schema.asset import Asset

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select

class AssetRepository:

    @staticmethod
    async def upsert(db: AsyncSession, asset_data: dict):
        # تعريف الـ Insert مع خاصية ON CONFLICT
        stmt = insert(Asset).values(asset_data)
        
        # في حال وجود تعارض في الـ ID، قم بتحديث الحقول التالية:
        stmt = stmt.on_conflict_do_update(
            index_elements=['id'],
            set_={
                'value': stmt.excluded.value,
                'status': stmt.excluded.status,
                'metadata_json': stmt.excluded.metadata_json,
                'last_seen': func.now()
            }
        )
        
        await db.execute(stmt)
        await db.commit()
        return {"status": "success", "id": asset_data['id']}

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

