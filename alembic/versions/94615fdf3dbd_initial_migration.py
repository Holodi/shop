"""Initial migration

Revision ID: 94615fdf3dbd
Revises: d870b9a30d56
Create Date: 2024-02-22 21:21:05.690111

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94615fdf3dbd'
down_revision: Union[str, None] = 'd870b9a30d56'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
