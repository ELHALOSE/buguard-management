from src.routes.schema.asset import (
    AssetCreate,
    AssetResponse
)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.model.database import get_db
from src.routes.schema.asset import AssetImportSchema
from src.model.AssetServiceLayer import AssetService

router = APIRouter(prefix="/api/v1/assets", tags=["Assets"])


# @router.post("",response_model=AssetResponse)
# async def create_asset(
#     payload: AssetCreate,
#     db: AsyncSession = Depends(get_db)
# ):
#     return await AssetService.upsert_asset(
#         db,
#         payload
#     )


# @router.get("",response_model=list[AssetResponse])
# async def get_assets(
#     db: AsyncSession = Depends(get_db)
# ):
#     return await AssetService.get_all_assets(
#         db
#     )


@router.get("/{asset_id}",response_model=AssetResponse)
async def get_asset(
    asset_id: str,
    db: AsyncSession = Depends(get_db)
):
    return await AssetService.get_by_id_asset(
        db,
        asset_id
    )


# it is a new endpoint to import assets from a list of AssetImportSchema
@router.post("/import")
async def import_assets(assets: List[AssetImportSchema], db: AsyncSession = Depends(get_db)):
    try:
        imported_count = 0
        for asset_data in assets:
            await AssetService.upsert_asset(db, asset_data)
            imported_count += 1
            
        return {
            "status": "success",
            "message": f"Successfully processed and merged {imported_count} assets."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))