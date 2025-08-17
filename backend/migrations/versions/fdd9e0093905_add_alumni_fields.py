"""add alumni graduation year and identity fields

Revision ID: fdd9e0093905
Revises: 201331d635c5
Create Date: 2025-08-15 16:35:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fdd9e0093905'
down_revision = '201331d635c5'
branch_labels = None
depends_on = None


def upgrade():
    """Add graduation year and alumni identity fields to members table."""
    # 添加畢業年級字段
    op.add_column('members', sa.Column('graduation_year', sa.Integer, nullable=True, comment='畢業年級'))
    
    # 添加校友身份字段 - 存儲校友的身份信息（如：研究生、博士生、教職員等）
    op.add_column('members', sa.Column('alumni_identity', sa.Integer, nullable=True, comment='校友身份類型'))
    
    # 添加索引用於校友排序查詢
    op.create_index('ix_member_alumni_graduation', 'members', ['mem_type', 'graduation_year'])
    op.create_index('ix_member_alumni_identity', 'members', ['mem_type', 'alumni_identity'])


def downgrade():
    """Remove graduation year and alumni identity fields from members table."""
    # 刪除索引
    op.drop_index('ix_member_alumni_identity', table_name='members')
    op.drop_index('ix_member_alumni_graduation', table_name='members')
    
    # 刪除字段
    op.drop_column('members', 'alumni_identity')
    op.drop_column('members', 'graduation_year')