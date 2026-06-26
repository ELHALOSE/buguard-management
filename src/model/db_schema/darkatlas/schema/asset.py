import uuid
from sqlalchemy import Column, String, DateTime, JSON, Enum as SQLEnum
from sqlalchemy.sql import func
from .darkatlas_base import SQLAlchemyBase 
from sqlalchemy.orm import relationship
from ..enums.AssetStatusEnum import AssetStatus
from ..enums.AssetTypeEnum import AssetType

class Asset(SQLAlchemyBase):
    __tablename__ = "assets"

    # هذا التعديل يسمح لك بإدخال id يدوي، وإذا تركته فارغاً سيتم توليد UUID
    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    type = Column(SQLEnum(AssetType), nullable=False)
    value = Column(String, nullable=False, index=True)
    status = Column(SQLEnum(AssetStatus), nullable=False, default=AssetStatus.ACTIVE)
    source = Column(String)
    tags = Column(JSON, default=list)
    metadata_json = Column(JSON, default=dict)
    first_seen = Column(DateTime(timezone=True), server_default=func.now())
    last_seen = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # استخدم String في تعريف العلاقات لتجنب الـ Circular Import
    outgoing_relationships = relationship(
        "AssetRelationship",
        foreign_keys="[AssetRelationship.source_asset_id]",
        back_populates="source_asset"
    )

    incoming_relationships = relationship(
        "AssetRelationship",
        foreign_keys="[AssetRelationship.target_asset_id]",
        back_populates="target_asset"
    )