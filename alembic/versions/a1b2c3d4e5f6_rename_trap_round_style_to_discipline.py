"""rename trap_round.style to discipline

Revision ID: a1b2c3d4e5f6
Revises: ff1d3dfb3a6b
Create Date: 2026-05-08 21:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = 'ff1d3dfb3a6b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('trap_round', 'style', new_column_name='discipline')


def downgrade() -> None:
    op.alter_column('trap_round', 'discipline', new_column_name='style')
