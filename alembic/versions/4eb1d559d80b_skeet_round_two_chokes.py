"""skeet round two chokes

Revision ID: 4eb1d559d80b
Revises: 9bf2d8a131e5
Create Date: 2026-06-14 20:23:14.444362

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4eb1d559d80b'
down_revision: Union[str, None] = '9bf2d8a131e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Rename the existing single choke column to choke 1 (preserves data, FK, index)
    op.alter_column('skeet_round', 'shotgun_choke_id', new_column_name='shotgun_choke_id1')
    op.execute('ALTER INDEX ix_skeet_round_shotgun_choke_id RENAME TO ix_skeet_round_shotgun_choke_id1')

    # Add a second choke column for skeet doubles
    op.add_column('skeet_round', sa.Column('shotgun_choke_id2', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_skeet_round_shotgun_choke_id2'), 'skeet_round', ['shotgun_choke_id2'], unique=False)
    op.create_foreign_key(None, 'skeet_round', 'shotgun_choke', ['shotgun_choke_id2'], ['id'], onupdate='CASCADE', ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('skeet_round_shotgun_choke_id2_fkey', 'skeet_round', type_='foreignkey')
    op.drop_index(op.f('ix_skeet_round_shotgun_choke_id2'), table_name='skeet_round')
    op.drop_column('skeet_round', 'shotgun_choke_id2')

    op.execute('ALTER INDEX ix_skeet_round_shotgun_choke_id1 RENAME TO ix_skeet_round_shotgun_choke_id')
    op.alter_column('skeet_round', 'shotgun_choke_id1', new_column_name='shotgun_choke_id')
