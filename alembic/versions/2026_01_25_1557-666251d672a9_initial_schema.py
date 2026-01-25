"""initial schema

Revision ID: 666251d672a9
Revises: 
Create Date: 2026-01-25 15:57:21.100205

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '666251d672a9'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('swipe',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('user1_id', sa.BigInteger(), nullable=False),
    sa.Column('user1_decision', sa.Boolean(), nullable=True),
    sa.Column('user2_id', sa.BigInteger(), nullable=False),
    sa.Column('user2_decision', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_swipe'))
    )
    op.create_table('user',
    sa.Column('telegram_id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('city', sa.String(length=30), nullable=False),
    sa.Column('description', sa.String(length=400), nullable=True),
    sa.Column('gender', sa.Enum('MALE', 'FEMALE', name='gender'), nullable=False),
    sa.Column('prefer_gender', sa.Enum('MALE', 'FEMALE', 'ANYONE', name='prefergender'), nullable=False),
    sa.PrimaryKeyConstraint('telegram_id', name=op.f('pk_user'))
    )
    op.create_table('photo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('file_id', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.telegram_id'], name=op.f('fk_photo_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_photo'))
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('photo')
    op.drop_table('user')
    op.drop_table('swipe')
