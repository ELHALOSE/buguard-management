from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.model.database import get_db

from src.model.AssetServiceLayer import AssetService

from src.routes.schema.asset import (
    AssetCreate,
    AssetResponse
)

router = APIRouter(
    prefix="/assets",
    tags=["Assets"]
)


@router.post("",response_model=AssetResponse)
async def create_asset(
    payload: AssetCreate,
    db: AsyncSession = Depends(get_db)
):
    return await AssetService.create_asset(
        db,
        payload
    )


@router.get("",response_model=list[AssetResponse])
async def get_assets(
    db: AsyncSession = Depends(get_db)
):
    return await AssetService.get_all_assets(
        db
    )


@router.get("/{asset_id}",response_model=AssetResponse)
async def get_asset(
    asset_id: str,
    db: AsyncSession = Depends(get_db)
):
    return await AssetService.get_by_id_asset(
        db,
        asset_id
    )
