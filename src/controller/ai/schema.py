from typing import Optional

from pydantic import BaseModel


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