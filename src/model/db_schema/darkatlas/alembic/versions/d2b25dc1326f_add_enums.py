"""add enums

Revision ID: d2b25dc1326f
Revises: 85c1b4f637f2
Create Date: 2026-06-25 19:09:58.616239
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = 'd2b25dc1326f'
down_revision: Union[str, Sequence[str], None] = '85c1b4f637f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


asset_type_enum = postgresql.ENUM(
    'DOMAIN',
    'SUBDOMAIN',
    'IP_ADDRESS',
    'SERVICE',
    'CERTIFICATE',
    'TECHNOLOGY',
    name='assettype'
)

asset_status_enum = postgresql.ENUM(
    'ACTIVE',
    'STALE',
    'ARCHIVED',
    name='assetstatus'
)


def upgrade() -> None:

    bind = op.get_bind()

    asset_type_enum.create(bind, checkfirst=True)
    asset_status_enum.create(bind, checkfirst=True)

    op.execute("""
        ALTER TABLE assets
        ALTER COLUMN type TYPE assettype
        USING type::assettype
    """)

    op.execute("""
        ALTER TABLE assets
        ALTER COLUMN status TYPE assetstatus
        USING status::assetstatus
    """)


def downgrade() -> None:

    bind = op.get_bind()

    op.execute("""
        ALTER TABLE assets
        ALTER COLUMN status TYPE VARCHAR
        USING status::text
    """)

    op.execute("""
        ALTER TABLE assets
        ALTER COLUMN type TYPE VARCHAR
        USING type::text
    """)

    asset_status_enum.drop(bind, checkfirst=True)
    asset_type_enum.drop(bind, checkfirst=True)