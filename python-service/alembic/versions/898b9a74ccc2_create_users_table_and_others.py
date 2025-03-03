"""Create users table

Revision ID: e61979fcfa2b
Revises: 2518ff8984ea
Create Date: 2025-03-03 14:48:51.818283

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e61979fcfa2b'
down_revision = '2518ff8984ea'
branch_labels = None
depends_on = None


def upgrade():
    # Create the users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('password_hash', sa.String(length=256), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Create the departments table
    op.create_table(
        'departments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # Create the sources table
    op.create_table(
        'sources',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('url', sa.String(length=255), nullable=True),
        sa.Column('source_type', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create the studies table
    op.create_table(
        'studies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('authors', sa.String(length=500), nullable=True),
        sa.Column('publication_date', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create the reference_ranges table - this must come after its dependencies
    op.create_table(
        'reference_ranges',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('test_name', sa.String(length=255), nullable=False),
        sa.Column('min_value', sa.Float(), nullable=True),
        sa.Column('max_value', sa.Float(), nullable=True),
        sa.Column('units', sa.String(length=50), nullable=True),
        sa.Column('department_id', sa.Integer(), nullable=False),
        sa.Column('source_id', sa.Integer(), nullable=True),
        sa.Column('study_id', sa.Integer(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id']),
        sa.ForeignKeyConstraint(['source_id'], ['sources.id']),
        sa.ForeignKeyConstraint(['study_id'], ['studies.id']),
        sa.ForeignKeyConstraint(['created_by'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    # Drop tables in reverse order (tables with foreign keys first)
    op.drop_table('reference_ranges')
    op.drop_table('studies')
    op.drop_table('sources')
    op.drop_table('departments')
    op.drop_table('users')