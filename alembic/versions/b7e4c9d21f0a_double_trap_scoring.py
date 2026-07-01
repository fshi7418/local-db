"""double trap scoring

Revision ID: b7e4c9d21f0a
Revises: 59cd12bb5d54
Create Date: 2026-07-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'b7e4c9d21f0a'
down_revision: Union[str, None] = '59cd12bb5d54'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('double_trap_round',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('firearm_end_id', sa.Integer(), nullable=False),
    sa.Column('distance_yard', sa.Float(), nullable=True),
    sa.Column('distance_m', sa.Float(), nullable=True),
    sa.Column('discipline', sa.String(), nullable=True),
    sa.Column('num_break', sa.SmallInteger(), nullable=True),
    sa.Column('starting_station', sa.SmallInteger(), nullable=True),
    sa.Column('shotgun_choke_id1', sa.Integer(), nullable=True),
    sa.Column('shotgun_choke_id2', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['firearm_end_id'], ['firearm_end.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['shotgun_choke_id1'], ['shotgun_choke.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['shotgun_choke_id2'], ['shotgun_choke.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_double_trap_round_firearm_end_id'), 'double_trap_round', ['firearm_end_id'], unique=False)
    op.create_table('double_trap_shot',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('double_trap_round_id', sa.Integer(), nullable=False),
    sa.Column('station', sa.Integer(), nullable=False),
    sa.Column('num_break', sa.SmallInteger(), nullable=False),
    sa.ForeignKeyConstraint(['double_trap_round_id'], ['double_trap_round.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_double_trap_shot_double_trap_round_id'), 'double_trap_shot', ['double_trap_round_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_double_trap_shot_double_trap_round_id'), table_name='double_trap_shot')
    op.drop_table('double_trap_shot')
    op.drop_index(op.f('ix_double_trap_round_firearm_end_id'), table_name='double_trap_round')
    op.drop_table('double_trap_round')
