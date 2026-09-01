"""trap round two chokes

Revision ID: cf05efc480eb
Revises: f4ab8e7d46f0
Create Date: 2026-08-30 18:56:25.840313

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cf05efc480eb'
down_revision: Union[str, None] = 'f4ab8e7d46f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Rename the existing single choke column to choke 1 (preserves data, FK, index)
    op.alter_column('trap_round', 'shotgun_choke_id', new_column_name='shotgun_choke_id1')
    op.execute('ALTER INDEX ix_trap_round_shotgun_choke_id RENAME TO ix_trap_round_shotgun_choke_id1')

    # Add a second choke column for disciplines allowing a second shot at the same target
    op.add_column('trap_round', sa.Column('shotgun_choke_id2', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_trap_round_shotgun_choke_id2'), 'trap_round', ['shotgun_choke_id2'], unique=False)
    op.create_foreign_key(None, 'trap_round', 'shotgun_choke', ['shotgun_choke_id2'], ['id'], onupdate='CASCADE', ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('trap_round_shotgun_choke_id2_fkey', 'trap_round', type_='foreignkey')
    op.drop_index(op.f('ix_trap_round_shotgun_choke_id2'), table_name='trap_round')
    op.drop_column('trap_round', 'shotgun_choke_id2')

    op.execute('ALTER INDEX ix_trap_round_shotgun_choke_id1 RENAME TO ix_trap_round_shotgun_choke_id')
    op.alter_column('trap_round', 'shotgun_choke_id1', new_column_name='shotgun_choke_id')
