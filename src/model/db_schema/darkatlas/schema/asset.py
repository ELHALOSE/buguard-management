import uuid

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import JSON

from sqlalchemy.sql import func
from .darkatlas_base import SQLAlchemyBase 

class Asset(SQLAlchemyBase):
    __tablename__ = "assets"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    type = Column(String, nullable=False)

    value = Column(
        String,
        nullable=False,
        index=True
    )

    status = Column(
        String,
        nullable=False,
        default="active"
    )

    source = Column(String)

    tags = Column(JSON, default=list)

    metadata_json = Column(JSON, default=dict)

    first_seen = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    last_seen = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )