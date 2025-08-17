"""make research_group_id and lab_id nullable for alumni

Revision ID: 42ea7a18a8b8
Revises: fdd9e0093905
Create Date: 2025-08-17 17:05:47.243290

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '42ea7a18a8b8'
down_revision = 'fdd9e0093905'
branch_labels = None
depends_on = None


def upgrade():
    """Make research_group_id and lab_id nullable to support alumni members."""
    # 獲取數據庫連接以檢查字段是否存在及其屬性
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {col['name']: col for col in inspector.get_columns('members')}
    
    # 只有當字段存在且當前為 NOT NULL 時才執行修改
    if 'research_group_id' in columns:
        col_info = columns['research_group_id']
        if not col_info.get('nullable', True):  # 如果當前不允許 NULL
            op.alter_column('members', 'research_group_id',
                            existing_type=sa.Integer(),
                            nullable=True)
    
    if 'lab_id' in columns:
        col_info = columns['lab_id']
        if not col_info.get('nullable', True):  # 如果當前不允許 NULL
            op.alter_column('members', 'lab_id',
                            existing_type=sa.Integer(),
                            nullable=True)


def downgrade():
    """Revert research_group_id and lab_id back to NOT NULL."""
    # 警告：這個操作可能會失敗，如果表中有 NULL 值
    # 獲取數據庫連接以檢查字段是否存在及其屬性
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {col['name']: col for col in inspector.get_columns('members')}
    
    # 只有當字段存在且當前為 NULL 時才執行修改
    if 'lab_id' in columns:
        col_info = columns['lab_id']
        if col_info.get('nullable', False):  # 如果當前允許 NULL
            op.alter_column('members', 'lab_id',
                            existing_type=sa.Integer(),
                            nullable=False)
    
    if 'research_group_id' in columns:
        col_info = columns['research_group_id']
        if col_info.get('nullable', False):  # 如果當前允許 NULL
            op.alter_column('members', 'research_group_id',
                            existing_type=sa.Integer(),
                            nullable=False)
