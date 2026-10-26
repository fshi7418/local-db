"""add skeet_round.sequence

Revision ID: a7c3e9d21b54
Revises: 34f546313bea
Create Date: 2026-10-25 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7c3e9d21b54'
down_revision: Union[str, None] = '34f546313bea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('skeet_round', sa.Column('sequence', sa.String(), nullable=True))
    # every round before this column shot the sequence of its own discipline
    op.execute('update skeet_round set sequence = discipline')


def downgrade() -> None:
    op.drop_column('skeet_round', 'sequence')
