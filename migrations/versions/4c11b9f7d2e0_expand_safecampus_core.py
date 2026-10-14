"""expand SafeCampus core workflow tables

Revision ID: 4c11b9f7d2e0
Revises: 1814fb7595f9
"""
from alembic import op
import sqlalchemy as sa

revision = "4c11b9f7d2e0"
down_revision = "1814fb7595f9"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("departments", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(120), nullable=False, unique=True), sa.Column("code", sa.String(30), nullable=False, unique=True), sa.Column("description", sa.Text()), sa.Column("is_active", sa.Boolean(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_departments_code", "departments", ["code"])
    with op.batch_alter_table("users") as batch:
        batch.add_column(sa.Column("registration_number", sa.String(64)))
        batch.add_column(sa.Column("faculty", sa.String(120)))
        batch.add_column(sa.Column("academic_department", sa.String(120)))
        batch.add_column(sa.Column("level", sa.String(20)))
        batch.add_column(sa.Column("role", sa.String(30), nullable=False, server_default="student"))
        batch.add_column(sa.Column("department_id", sa.Integer(), sa.ForeignKey("departments.id")))
        batch.create_unique_constraint("uq_users_registration_number", ["registration_number"])
        batch.create_index("ix_users_registration_number", ["registration_number"])
        batch.create_index("ix_users_role", ["role"])
        batch.create_index("ix_users_department_id", ["department_id"])
    op.create_table("case_categories", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(100), nullable=False, unique=True), sa.Column("slug", sa.String(100), nullable=False, unique=True), sa.Column("department_id", sa.Integer(), sa.ForeignKey("departments.id")), sa.Column("is_health_sensitive", sa.Boolean(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_table("campus_cases", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("public_id", sa.String(20), nullable=False, unique=True), sa.Column("case_type", sa.String(30), nullable=False), sa.Column("priority", sa.String(20), nullable=False), sa.Column("status", sa.String(30), nullable=False), sa.Column("description", sa.Text(), nullable=False), sa.Column("location", sa.String(180)), sa.Column("is_sensitive", sa.Boolean(), nullable=False), sa.Column("reporter_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False), sa.Column("category_id", sa.Integer(), sa.ForeignKey("case_categories.id"), nullable=False), sa.Column("owner_department_id", sa.Integer(), sa.ForeignKey("departments.id")), sa.Column("assignee_id", sa.Integer(), sa.ForeignKey("users.id")), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_table("case_status_history", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("case_id", sa.Integer(), sa.ForeignKey("campus_cases.id", ondelete="CASCADE"), nullable=False), sa.Column("actor_id", sa.Integer(), sa.ForeignKey("users.id")), sa.Column("old_status", sa.String(30)), sa.Column("new_status", sa.String(30), nullable=False), sa.Column("note", sa.String(500)), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_table("case_comments", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("case_id", sa.Integer(), sa.ForeignKey("campus_cases.id", ondelete="CASCADE"), nullable=False), sa.Column("author_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False), sa.Column("body", sa.Text(), nullable=False), sa.Column("is_internal", sa.Boolean(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_table("notifications", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("title", sa.String(160), nullable=False), sa.Column("body", sa.String(500), nullable=False), sa.Column("link", sa.String(255)), sa.Column("read_at", sa.DateTime(timezone=True)), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_table("audit_logs", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("actor_id", sa.Integer(), sa.ForeignKey("users.id")), sa.Column("action", sa.String(100), nullable=False), sa.Column("resource_type", sa.String(60), nullable=False), sa.Column("resource_id", sa.String(80), nullable=False), sa.Column("detail", sa.String(500)), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_table("lost_found_items", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("public_id", sa.String(20), nullable=False, unique=True), sa.Column("kind", sa.String(10), nullable=False), sa.Column("title", sa.String(160), nullable=False), sa.Column("description", sa.Text(), nullable=False), sa.Column("location", sa.String(180)), sa.Column("event_date", sa.Date()), sa.Column("status", sa.String(20), nullable=False), sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_table("safety_alerts", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("title", sa.String(160), nullable=False), sa.Column("location", sa.String(180)), sa.Column("severity", sa.String(20), nullable=False), sa.Column("message", sa.Text(), nullable=False), sa.Column("is_active", sa.Boolean(), nullable=False), sa.Column("issued_by_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))


def downgrade():
    op.drop_table("safety_alerts"); op.drop_table("lost_found_items"); op.drop_table("audit_logs"); op.drop_table("notifications"); op.drop_table("case_comments"); op.drop_table("case_status_history")
    op.drop_table("campus_cases")
    op.drop_table("case_categories")
    with op.batch_alter_table("users") as batch:
        batch.drop_column("department_id"); batch.drop_column("role"); batch.drop_column("level"); batch.drop_column("academic_department"); batch.drop_column("faculty"); batch.drop_column("registration_number")
    op.drop_index("ix_departments_code", table_name="departments")
    op.drop_table("departments")
