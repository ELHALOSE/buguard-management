from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.model.database import get_db
from src.controller.ai.query_chain import process_natural_language_query

router = APIRouter(prefix="/api/v1/query", tags=["NLPQuery"])

class NLQueryRequest(BaseModel):
    question: str

@router.post("/query")
async def ask_database(payload: NLQueryRequest, db: AsyncSession = Depends(get_db)):
    """
    EX: "Show me all active domains"
    """
    response = await process_natural_language_query(db, payload.question)
    
    if "error" in response:
        # إرجاع خطأ 400 إذا كان السؤال خارج النطاق أو خبيثاً
        raise HTTPException(status_code=400, detail=response["error"])
        
    return response