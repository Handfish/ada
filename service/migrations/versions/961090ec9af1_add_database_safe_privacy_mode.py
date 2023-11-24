"""add database safe/privacy mode

Revision ID: 961090ec9af1
Revises: b7c451b82bc1
Create Date: 2023-11-24 22:27:22.529506

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '961090ec9af1'
down_revision: Union[str, None] = 'b7c451b82bc1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('database', sa.Column('safe_mode', sa.Boolean(), server_default='true', nullable=False))
    op.add_column('database', sa.Column('privacy_mode', sa.Boolean(), server_default='true', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('database', 'privacy_mode')
    op.drop_column('database', 'safe_mode')
    # ### end Alembic commands ###