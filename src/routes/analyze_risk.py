from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.model.database import get_db
from src.controller.ai.query_chain import  analyze_asset_risk
from src.model.AssetServiceLayer import AssetService

router = APIRouter(prefix="/api/v1/risk", tags=["RiskAnalysis"])

@router.post("/analyze/{asset_id}")
async def analyze_risk(asset_id: str, db: AsyncSession = Depends(get_db)):
    # 1. جلب بيانات الأصل من الـ Service
    asset = await AssetService.get_by_id_asset(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    # 2. تحليل المخاطر باستخدام AI
    # نحول بيانات الأصل لـ dict قبل الإرسال
    asset_dict = {"value": asset.value, "type": asset.type, "metadata": asset.metadata_json}
    risk_report = await analyze_asset_risk(asset_dict)
    
    return risk_report