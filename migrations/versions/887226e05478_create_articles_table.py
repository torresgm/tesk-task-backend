"""Create articles table

Revision ID: 887226e05478
Revises: 
Create Date: 2024-05-31 13:52:47.944354

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '887226e05478'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
table_name = "articles"


def upgrade() -> None:
    op.create_table(
        table_name,
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("summary", sa.Text, nullable=True),
    )


def downgrade() -> None:
    op.drop_table(table_name)
