"""Create monitors table

Revision ID: 0001_create_monitors
Revises: None
Create Date: 2026-09-05 12:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0001_create_monitors"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "monitors",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("url", sa.String(length=2048), nullable=False),
        sa.Column("type", sa.String(length=10), nullable=False, server_default="HTTP"),
        sa.Column("interval", sa.Integer(), nullable=False, server_default="60"),
        sa.Column("timeout", sa.Integer(), nullable=False, server_default="5"),
        sa.Column(
            "expected_status", sa.Integer(), nullable=False, server_default="200"
        ),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_monitors_id"), "monitors", ["id"], unique=False)
    op.create_index(op.f("ix_monitors_name"), "monitors", ["name"], unique=False)
    op.create_index(op.f("ix_monitors_user_id"), "monitors", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_monitors_user_id"), table_name="monitors")
    op.drop_index(op.f("ix_monitors_name"), table_name="monitors")
    op.drop_index(op.f("ix_monitors_id"), table_name="monitors")
    op.drop_table("monitors")
