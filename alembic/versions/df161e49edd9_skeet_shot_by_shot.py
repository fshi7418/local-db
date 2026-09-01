"""skeet shot by shot

Revision ID: df161e49edd9
Revises: 890f36767f46
Create Date: 2026-08-31 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'df161e49edd9'
down_revision: Union[str, None] = '890f36767f46'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # skeet_shot is empty, so the new columns can go straight in as NOT NULL
    op.add_column('skeet_shot', sa.Column('shot_order', sa.SmallInteger(), nullable=False))
    op.add_column('skeet_shot', sa.Column('target_number', sa.SmallInteger(), nullable=False))
    op.add_column('skeet_shot', sa.Column('house', sa.String(), nullable=False))
    op.add_column('skeet_shot', sa.Column('single_double', sa.String(), nullable=False))
    op.add_column('skeet_shot', sa.Column('pair_order', sa.SmallInteger(), nullable=True))
    op.add_column('skeet_shot', sa.Column('is_option', sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column('skeet_shot', sa.Column('broken', sa.Boolean(), nullable=False))
    op.alter_column('skeet_shot', 'is_option', server_default=None)
    op.drop_column('skeet_shot', 'is_doubles')
    op.drop_column('skeet_shot', 'num_break')


def downgrade() -> None:
    op.add_column('skeet_shot', sa.Column('num_break', sa.SMALLINT(), autoincrement=False, nullable=True))
    op.add_column('skeet_shot', sa.Column('is_doubles', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_column('skeet_shot', 'broken')
    op.drop_column('skeet_shot', 'is_option')
    op.drop_column('skeet_shot', 'pair_order')
    op.drop_column('skeet_shot', 'single_double')
    op.drop_column('skeet_shot', 'house')
    op.drop_column('skeet_shot', 'target_number')
    op.drop_column('skeet_shot', 'shot_order')
