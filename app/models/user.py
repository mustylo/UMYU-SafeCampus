from datetime import datetime, timezone
from uuid import uuid4

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError
from flask_login import UserMixin

from app.extensions import db

password_hasher = PasswordHasher()


class TimestampMixin:
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class Department(TimestampMixin, db.Model):
    __tablename__ = "departments"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    code = db.Column(db.String(30), nullable=False, unique=True, index=True)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)


class User(UserMixin, TimestampMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(30), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    account_status = db.Column(db.String(20), nullable=False, default="active")
    registration_number = db.Column(db.String(64), unique=True, nullable=True, index=True)
    faculty = db.Column(db.String(120), nullable=True)
    academic_department = db.Column(db.String(120), nullable=True)
    level = db.Column(db.String(20), nullable=True)
    role = db.Column(db.String(30), nullable=False, default="student", index=True)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=True, index=True)
    department = db.relationship("Department", foreign_keys=[department_id])

    def set_password(self, password):
        self.password_hash = password_hasher.hash(password)

    def check_password(self, password):
        try:
            return password_hasher.verify(self.password_hash, password)
        except (VerifyMismatchError, InvalidHashError):
            return False

    @property
    def is_active(self):
        return self.account_status == "active"

    def has_role(self, *roles):
        return self.role in roles


class CaseCategory(TimestampMixin, db.Model):
    __tablename__ = "case_categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    slug = db.Column(db.String(100), nullable=False, unique=True, index=True)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=True)
    department = db.relationship("Department")
    is_health_sensitive = db.Column(db.Boolean, nullable=False, default=False)


class CampusCase(TimestampMixin, db.Model):
    __tablename__ = "campus_cases"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(20), unique=True, nullable=False, default=lambda: f"SC-{uuid4().hex[:12].upper()}", index=True)
    case_type = db.Column(db.String(30), nullable=False, default="service_request")
    priority = db.Column(db.String(20), nullable=False, default="medium")
    status = db.Column(db.String(30), nullable=False, default="submitted", index=True)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(180), nullable=True)
    is_sensitive = db.Column(db.Boolean, nullable=False, default=False)
    reporter_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey("case_categories.id"), nullable=False)
    owner_department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=True, index=True)
    assignee_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True, index=True)
    reporter = db.relationship("User", foreign_keys=[reporter_id])
    category = db.relationship("CaseCategory")
    owner_department = db.relationship("Department", foreign_keys=[owner_department_id])
    assignee = db.relationship("User", foreign_keys=[assignee_id])


class CaseStatusHistory(TimestampMixin, db.Model):
    __tablename__ = "case_status_history"
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey("campus_cases.id", ondelete="CASCADE"), nullable=False, index=True)
    actor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    old_status = db.Column(db.String(30), nullable=True)
    new_status = db.Column(db.String(30), nullable=False)
    note = db.Column(db.String(500), nullable=True)
    case = db.relationship("CampusCase", backref=db.backref("status_history", cascade="all, delete-orphan", order_by="CaseStatusHistory.created_at"))
    actor = db.relationship("User")


class CaseComment(TimestampMixin, db.Model):
    __tablename__ = "case_comments"
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey("campus_cases.id", ondelete="CASCADE"), nullable=False, index=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    body = db.Column(db.Text, nullable=False)
    is_internal = db.Column(db.Boolean, nullable=False, default=False)
    case = db.relationship("CampusCase", backref=db.backref("comments", cascade="all, delete-orphan", order_by="CaseComment.created_at"))
    author = db.relationship("User")


class Notification(TimestampMixin, db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = db.Column(db.String(160), nullable=False)
    body = db.Column(db.String(500), nullable=False)
    link = db.Column(db.String(255), nullable=True)
    read_at = db.Column(db.DateTime(timezone=True), nullable=True)
    user = db.relationship("User")


class AuditLog(TimestampMixin, db.Model):
    __tablename__ = "audit_logs"
    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    action = db.Column(db.String(100), nullable=False)
    resource_type = db.Column(db.String(60), nullable=False)
    resource_id = db.Column(db.String(80), nullable=False)
    detail = db.Column(db.String(500), nullable=True)
    actor = db.relationship("User")


class LostFoundItem(TimestampMixin, db.Model):
    __tablename__ = "lost_found_items"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(20), unique=True, nullable=False, default=lambda: f"LF-{uuid4().hex[:12].upper()}", index=True)
    kind = db.Column(db.String(10), nullable=False)
    title = db.Column(db.String(160), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(180), nullable=True)
    event_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), nullable=False, default="open")
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    owner = db.relationship("User")


class SafetyAlert(TimestampMixin, db.Model):
    __tablename__ = "safety_alerts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    location = db.Column(db.String(180), nullable=True)
    severity = db.Column(db.String(20), nullable=False, default="medium")
    message = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    issued_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    issued_by = db.relationship("User")
