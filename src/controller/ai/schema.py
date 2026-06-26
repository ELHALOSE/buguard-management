from typing import Optional
from pydantic import BaseModel, Field

class AssetQuery(BaseModel):
    type: Optional[str] = None
    status: Optional[str] = None
    source: Optional[str] = None
    tag: Optional[str] = None



class AssetSearchFilter(BaseModel):
    type: Optional[str] = None
    status: Optional[str] = None
    source: Optional[str] = None
    tag: Optional[str] = None



class RiskAssessment(BaseModel):
    score: int = Field(description="Risk score from 1 to 10")
    summary: str = Field(description="Brief summary of why this asset is risky")
    critical_issues: list[str] = Field(description="2 List of specific critical security issues")