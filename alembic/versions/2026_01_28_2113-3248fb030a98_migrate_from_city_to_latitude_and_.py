"""migrate from city to latitude and longitude

Revision ID: 3248fb030a98
Revises: 666251d672a9
Create Date: 2026-01-28 21:13:30.627888

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '3248fb030a98'
down_revision: Union[str, Sequence[str], None] = '666251d672a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('user', sa.Column('longitude', sa.Float(), nullable=False, server_default='0.0'))
    op.add_column('user', sa.Column('latitude', sa.Float(), nullable=False, server_default='0.0'))
    op.drop_column('user', 'city')

def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('user', sa.Column('city', sa.VARCHAR(length=30), autoincrement=False, nullable=False))
    op.drop_column('user', 'latitude')
    op.drop_column('user', 'longitude')