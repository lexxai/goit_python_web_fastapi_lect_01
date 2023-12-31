"""'refresh'

Revision ID: e0e04f78f8a5
Revises: d0b825141d11
Create Date: 2023-11-09 05:24:23.817750

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e0e04f78f8a5'
down_revision: Union[str, None] = 'd0b825141d11'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('refresh_token', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'refresh_token')
    # ### end Alembic commands ###
