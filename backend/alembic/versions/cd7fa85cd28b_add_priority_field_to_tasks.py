"""add_priority_field_to_tasks

Revision ID: cd7fa85cd28b
Revises: 81b01a445bb1
Create Date: 2025-05-14 10:51:29.917697

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision: str = 'cd7fa85cd28b'
down_revision: Union[str, None] = '81b01a445bb1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create a temporary table reference
    tasks = table('tasks',
        column('priority', sa.String)
    )

    # Add priority column as nullable first
    op.add_column('tasks', sa.Column('priority', sa.String(), nullable=True))
    
    # Set default value for existing rows
    op.execute(tasks.update().values(priority='medium'))
    
    # Make the column not nullable
    op.alter_column('tasks', 'priority',
        existing_type=sa.String(),
        nullable=False
    )


def downgrade() -> None:
    # Remove priority column
    op.drop_column('tasks', 'priority')
