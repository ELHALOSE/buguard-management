import uuid

from sqlalchemy import Column, String, ForeignKey

from .darkatlas_base import SQLAlchemyBase
from sqlalchemy.orm import relationship

class AssetRelationship(SQLAlchemyBase):
    __tablename__ = "asset_relationships"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    source_asset_id = Column(
        String,
        ForeignKey("assets.id"),
        nullable=False
    )

    target_asset_id = Column(
        String,
        ForeignKey("assets.id"),
        nullable=False
    )

    relationship_type = Column(
        String,
        nullable=False
    )


    source_asset = relationship(
            "Asset",
            foreign_keys=[source_asset_id],
            back_populates="outgoing_relationships" # مطابق للاسم في Asset
        )

    target_asset = relationship(
        "Asset",
        foreign_keys=[target_asset_id],
        back_populates="incoming_relationships" # مطابق للاسم في Asset
    )