import re

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from app.extensions import db, limiter
from app.models import AuditLog, User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _register_values():
    return {key: (request.form.get(key) or "").strip() for key in ("full_name", "email", "phone", "registration_number", "faculty", "academic_department", "level")}


@auth_bp.route("/register", methods=["GET", "POST"])
@limiter.limit("5 per hour")
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    values = _register_values()
    if request.method == "POST":
        password = request.form.get("password") or ""
        confirm = request.form.get("confirm_password") or ""
        errors = []
        if len(values["full_name"]) < 2: errors.append("Enter your full name.")
        if not EMAIL_RE.fullmatch(values["email"].lower()): errors.append("Enter a valid email address.")
        if not values["registration_number"]: errors.append("Registration number is required.")
        if not values["faculty"] or not values["academic_department"] or not values["level"]: errors.append("Faculty, academic department and level are required.")
        if len(password) < 12: errors.append("Choose a password of at least 12 characters.")
        if password != confirm: errors.append("Password confirmation does not match.")
        if User.query.filter_by(email=values["email"].lower()).first(): errors.append("This email is already registered.")
        if User.query.filter_by(registration_number=values["registration_number"].upper()).first(): errors.append("This registration number is already registered.")
        if errors:
            for error in errors: flash(error, "error")
        else:
            values["email"] = values["email"].lower()
            values["registration_number"] = values["registration_number"].upper()
            user = User(**values)
            user.set_password(password)
            db.session.add(user)
            db.session.flush()
            db.session.add(AuditLog(actor_id=user.id, action="account_registered", resource_type="user", resource_id=str(user.id)))
            db.session.commit()
            login_user(user)
            flash("Your account was created. Welcome to SafeCampus.", "success")
            return redirect(url_for("main.dashboard"))
    return render_template("auth/register.html", values=values)


@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("10 per hour")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash("Invalid email or password.", "error")
        elif not user.is_active:
            flash("This account is not active. Please contact an administrator.", "error")
        else:
            login_user(user)
            db.session.add(AuditLog(actor_id=user.id, action="login", resource_type="user", resource_id=str(user.id)))
            db.session.commit()
            return redirect(request.args.get("next") or url_for("main.dashboard"))
    return render_template("auth/login.html")


@auth_bp.post("/logout")
def logout():
    if current_user.is_authenticated:
        db.session.add(AuditLog(actor_id=current_user.id, action="logout", resource_type="user", resource_id=str(current_user.id)))
        db.session.commit()
    logout_user()
    flash("You have been signed out.", "success")
    return redirect(url_for("main.home"))
