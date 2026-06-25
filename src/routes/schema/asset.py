from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class AssetCreate(BaseModel):
    type: str
    value: str
    status: str = "active"
    source: Optional[str] = None
    tags: list[str] = []
    metadata_json: dict = {}


class AssetResponse(BaseModel):
    id: str
    type: str
    value: str
    status: str
    source: Optional[str]
    tags: list[str]
    metadata_json: dict

    class Config:
        from_attributes = True

class AssetImportSchema(BaseModel):
    id: str
    type: str
    value: str
    status: str
    source: str
    tags: Optional[List[str]] = []
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, alias="metadata")
    # حقول إضافية للعلاقات (اختيارية)
    parent: Optional[str] = None 
    covers: Optional[str] = None


