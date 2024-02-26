"""Initial migration

Revision ID: d870b9a30d56
Revises: fd26793818cc
Create Date: 2024-02-22 21:17:40.467449

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd870b9a30d56'
down_revision: Union[str, None] = 'fd26793818cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
