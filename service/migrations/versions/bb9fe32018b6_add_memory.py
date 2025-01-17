"""add memory

Revision ID: bb9fe32018b6
Revises: 2af9b2c6c9ea
Create Date: 2023-08-31 22:39:52.068601

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb9fe32018b6'
down_revision: Union[str, None] = '2af9b2c6c9ea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('database', sa.Column('memory', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('database', 'memory')
    # ### end Alembic commands ###
