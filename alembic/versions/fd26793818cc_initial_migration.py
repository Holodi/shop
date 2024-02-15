"""initial migration

Revision ID: fd26793818cc
Revises: 
Create Date: 2024-02-15 17:56:11.303692

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd26793818cc'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Таблиця user
    op.create_table(
        'user',
        sa.Column('login', sa.String(50), primary_key=True),
        sa.Column('name', sa.String(100)),
        sa.Column('password', sa.String(255)),
        sa.Column('phone', sa.String(20)),
        sa.Column('surname', sa.String(100)),
    )

    # Таблиця cart
    op.create_table(
        'cart',
        sa.Column('user_login', sa.String(50), sa.ForeignKey('user.login')),
        sa.Column('item_id', sa.Integer, sa.ForeignKey('item.id')),
        sa.Column('quantity', sa.Integer),
    )

    # Таблиця order
    op.create_table(
        'order',
        sa.Column('order_id', sa.Integer, primary_key=True),
        sa.Column('user_login', sa.String(50), sa.ForeignKey('user.login')),
        sa.Column('address', sa.String(255)),
        sa.Column('order_total_price', sa.Float),
        sa.Column('status', sa.String(20)),
    )

    # Таблиця category
    op.create_table(
        'category',
        sa.Column('cat_id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100)),
    )

    # Таблиця order_items
    op.create_table(
        'order_items',
        sa.Column('order_id', sa.Integer, sa.ForeignKey('order.order_id')),
        sa.Column('itm_id', sa.Integer, sa.ForeignKey('item.id')),
    )

    # Таблиця item
    op.create_table(
        'item',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255)),
        sa.Column('description', sa.Text),
        sa.Column('price', sa.Float),
        sa.Column('status', sa.String(20)),
        sa.Column('category', sa.Integer, sa.ForeignKey('category.cat_id')),
    )

    # Таблиця item_status
    op.create_table(
        'item_status',
        sa.Column('stat_id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50)),
    )

    # Таблиця waitlist
    op.create_table(
        'waitlist',
        sa.Column('user_login', sa.String(50), sa.ForeignKey('user.login')),
        sa.Column('item_id', sa.Integer, sa.ForeignKey('item.id')),
    )

    # Таблиця wishlist
    op.create_table(
        'wishlist',
        sa.Column('list_id', sa.Integer, primary_key=True),
        sa.Column('list_name', sa.String(100)),
        sa.Column('user_login', sa.String(50), sa.ForeignKey('user.login')),
        sa.Column('item_id', sa.Integer, sa.ForeignKey('item.id')),
    )

    # Таблиця order_status
    op.create_table(
        'order_status',
        sa.Column('stat_id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50)),
    )

    # Таблиця feedback
    op.create_table(
        'feedback',
        sa.Column('feedback_id', sa.Integer, primary_key=True),
        sa.Column('itm_id', sa.Integer, sa.ForeignKey('item.id')),
        sa.Column('text', sa.Text),
        sa.Column('rating', sa.Integer),
        sa.Column('user_login', sa.String(50), sa.ForeignKey('user.login')),
    )



def downgrade() -> None:
    pass
