from pydantic import BaseModel
from typing import Optional


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