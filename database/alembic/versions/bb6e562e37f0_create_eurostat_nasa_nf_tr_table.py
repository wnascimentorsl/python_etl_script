"""create_eurostat_nasa_nf_tr_table

Revision ID: bb6e562e37f0
Revises:
Create Date: 2026-07-07 07:25:35.716203

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb6e562e37f0'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'eurostat_nasa_nf_tr',
        sa.Column('id', sa.String(length=64), nullable=False),
        sa.Column('freq', sa.String(length=5), nullable=False),
        sa.Column('sector', sa.String(length=20), nullable=False),
        sa.Column('na_item', sa.String(length=20), nullable=False),
        sa.Column('geo', sa.String(length=20), nullable=False),
        sa.Column('unit', sa.String(length=20), nullable=False),
        sa.Column('direct', sa.String(length=4), nullable=False),
        sa.Column('time', sa.Integer(), nullable=False),
        sa.Column('value', sa.Numeric()),
        sa.Column('flag', sa.String(length=10)),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index('idx_eurostat_geo_time', 'eurostat_nasa_nf_tr', ['geo', 'time'], unique=False)
    op.create_index('idx_eurostat_sector_item', 'eurostat_nasa_nf_tr', ['sector', 'na_item'], unique=False)


def downgrade() -> None:
    op.drop_index('idx_eurostat_sector_item', table_name='eurostat_nasa_nf_tr')
    op.drop_index('idx_eurostat_geo_year', table_name='eurostat_nasa_nf_tr')
    op.drop_table('eurostat_nasa_nf_tr')
