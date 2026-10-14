from datetime import datetime, timezone
from functools import wraps

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.models import (AuditLog, CampusCase, CaseCategory, CaseComment,
                        CaseStatusHistory, LostFoundItem, Notification,
                        SafetyAlert, User)
from app.services.phishing import analyze

main_bp = Blueprint("main", __name__)
STAFF_ROLES = {"staff", "officer", "department_head", "admin"}
VALID_STATUSES = {"submitted", "under_review", "assigned", "in_progress", "completed", "verified", "resolved", "closed", "escalated", "rejected", "reopened"}


def roles_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.has_role(*roles): abort(403)
            return view(*args, **kwargs)
        return wrapped
    return decorator


def can_access_case(case):
    if current_user.id == case.reporter_id or current_user.has_role("admin"): return True
    if not current_user.has_role(*STAFF_ROLES): return False
    if case.is_sensitive and current_user.department_id != case.owner_department_id: return False
    return current_user.department_id == case.owner_department_id or current_user.id == case.assignee_id


def record(action, resource, detail=None):
    db.session.add(AuditLog(actor_id=current_user.id if current_user.is_authenticated else None, action=action, resource_type=resource.__class__.__name__, resource_id=str(resource.id), detail=detail))


@main_bp.get("/")
def home():
    alerts = SafetyAlert.query.filter_by(is_active=True).order_by(SafetyAlert.created_at.desc()).limit(3).all()
    return render_template("home.html", alerts=alerts)


@main_bp.get("/dashboard")
@login_required
def dashboard():
    if current_user.has_role(*STAFF_ROLES):
        query = CampusCase.query.filter_by(owner_department_id=current_user.department_id)
        return render_template("staff_dashboard.html", cases=query.order_by(CampusCase.updated_at.desc()).limit(12).all(), open_count=query.filter(CampusCase.status.notin_(["resolved", "closed"])).count())
    cases = CampusCase.query.filter_by(reporter_id=current_user.id).order_by(CampusCase.updated_at.desc()).limit(10).all()
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).limit(6).all()
    return render_template("dashboard.html", cases=cases, notifications=notifications)


@main_bp.route("/reports/new", methods=["GET", "POST"])
@login_required
def create_case():
    categories = CaseCategory.query.order_by(CaseCategory.name).all()
    if request.method == "POST":
        category = db.session.get(CaseCategory, request.form.get("category_id", type=int))
        description = (request.form.get("description") or "").strip()

        if not category or not description or len(description) > 5000:
            flash(
                "Choose a category and provide a description of up to 5,000 characters.",
                "error",
            )
        else:
            case = CampusCase(
                case_type=request.form.get("case_type", "service_request"),
                priority=request.form.get("priority", "medium"),
                description=description,
                location=(request.form.get("location") or "").strip()[:180] or None,
                reporter_id=current_user.id,
                category=category,
                owner_department=category.department,
                is_sensitive=category.is_health_sensitive,
            )
            db.session.add(case)
            db.session.flush()

            db.session.add(
                CaseStatusHistory(
                    case_id=case.id,
                    actor_id=current_user.id,
                    new_status="submitted",
                    note="Case submitted and routed.",
                )
            )
            record("case_created", case, "Automatically routed from category.")

            db.session.add(
                Notification(
                    user_id=current_user.id,
                    title="Report submitted",
                    body=f"Your report {case.public_id} was submitted.",
                    link=url_for("main.case_detail", public_id=case.public_id),
                )
            )
            db.session.commit()

            flash(f"Report {case.public_id} was submitted.", "success")
            return redirect(
                url_for("main.case_detail", public_id=case.public_id)
            )

    return render_template("case_form.html", categories=categories)

@main_bp.route("/reports/<public_id>", methods=["GET", "POST"])
@login_required
def case_detail(public_id):
    case = CampusCase.query.filter_by(public_id=public_id).first_or_404()
    if not can_access_case(case): abort(403)
    if request.method == "POST":
        body = (request.form.get("body") or "").strip()
        internal = request.form.get("internal") == "1"
        if not body or len(body) > 3000 or (internal and not current_user.has_role(*STAFF_ROLES)):
            flash("Comment could not be added.", "error")
        else:
            comment = CaseComment(case_id=case.id, author_id=current_user.id, body=body, is_internal=internal)
            db.session.add(comment); record("case_comment_added", case)
            if current_user.id != case.reporter_id and not internal:
                db.session.add(Notification(user_id=case.reporter_id, title="New report update", body=f"There is a new update on {case.public_id}.", link=url_for("main.case_detail", public_id=case.public_id)))
            db.session.commit(); flash("Update added.", "success")
            return redirect(url_for("main.case_detail", public_id=public_id))
    assignees = []
    if current_user.has_role("officer", "department_head", "admin") and case.owner_department_id:
        assignees = User.query.filter_by(department_id=case.owner_department_id, account_status="active").filter(User.role.in_(["staff", "officer", "department_head"])).order_by(User.full_name).all()
    return render_template("case_detail.html", case=case, assignees=assignees)


@main_bp.post("/reports/<public_id>/status")
@login_required
@roles_required(*STAFF_ROLES)
def update_case_status(public_id):
    case = CampusCase.query.filter_by(public_id=public_id).first_or_404()
    if not can_access_case(case): abort(403)
    new_status = request.form.get("status")
    if new_status not in VALID_STATUSES: abort(400)
    old_status = case.status; case.status = new_status
    db.session.add(CaseStatusHistory(case_id=case.id, actor_id=current_user.id, old_status=old_status, new_status=new_status, note=(request.form.get("note") or "")[:500]))
    db.session.add(Notification(user_id=case.reporter_id, title="Report status changed", body=f"{case.public_id} is now {new_status.replace('_', ' ')}.", link=url_for("main.case_detail", public_id=case.public_id)))
    record("case_status_changed", case, f"{old_status} -> {new_status}")
    db.session.commit(); flash("Status updated.", "success")
    return redirect(url_for("main.case_detail", public_id=public_id))


@main_bp.post("/reports/<public_id>/assign")
@login_required
@roles_required("officer", "department_head", "admin")
def assign_case(public_id):
    case = CampusCase.query.filter_by(public_id=public_id).first_or_404()
    if not can_access_case(case): abort(403)
    assignee = db.session.get(User, request.form.get("assignee_id", type=int))
    if not assignee or assignee.department_id != case.owner_department_id or not assignee.has_role("staff", "officer", "department_head"):
        flash("Choose an authorized staff member in the owning department.", "error")
        return redirect(url_for("main.case_detail", public_id=public_id))
    case.assignee = assignee
    old_status = case.status
    if case.status == "submitted": case.status = "assigned"
    db.session.add(CaseStatusHistory(case_id=case.id, actor_id=current_user.id, old_status=old_status, new_status=case.status, note=f"Assigned to {assignee.full_name}."))
    db.session.add(Notification(user_id=assignee.id, title="New assigned report", body=f"You were assigned {case.public_id}.", link=url_for("main.case_detail", public_id=case.public_id)))
    db.session.add(Notification(user_id=case.reporter_id, title="Report assigned", body=f"{case.public_id} was assigned for action.", link=url_for("main.case_detail", public_id=case.public_id)))
    record("case_assigned", case, f"Assigned to {assignee.id}")
    db.session.commit(); flash("Report assigned.", "success")
    return redirect(url_for("main.case_detail", public_id=public_id))


@main_bp.route("/cybersecurity/analyzer", methods=["GET", "POST"])
def phishing_analyzer():
    result = None
    if request.method == "POST":
        try: result = analyze(request.form.get("message"), request.form.get("url"))
        except ValueError as error: flash(str(error), "error")
    return render_template("analyzer.html", result=result)


@main_bp.route("/lost-found", methods=["GET", "POST"])
@login_required
def lost_found():
    if request.method == "POST":
        title, description = (request.form.get("title") or "").strip(), (request.form.get("description") or "").strip()
        kind = request.form.get("kind")
        if kind not in {"lost", "found"} or not title or not description: flash("Complete the lost/found form.", "error")
        else:
            item = LostFoundItem(kind=kind, title=title[:160], description=description[:3000], location=(request.form.get("location") or "").strip()[:180] or None, owner_id=current_user.id)
            db.session.add(item); db.session.flush(); record("lost_found_created", item); db.session.commit(); flash("Item submitted for controlled matching.", "success")
            return redirect(url_for("main.lost_found"))
    items = LostFoundItem.query.filter_by(status="open").order_by(LostFoundItem.created_at.desc()).all()
    return render_template("lost_found.html", items=items)


@main_bp.get("/alerts")
def alerts():
    return render_template("alerts.html", alerts=SafetyAlert.query.filter_by(is_active=True).order_by(SafetyAlert.created_at.desc()).all())


@main_bp.route("/alerts/new", methods=["GET", "POST"])
@login_required
@roles_required("officer", "department_head", "admin")
def create_alert():
    if request.method == "POST":
        title, message = (request.form.get("title") or "").strip(), (request.form.get("message") or "").strip()
        severity = request.form.get("severity", "medium")
        if not title or not message or severity not in {"low", "medium", "high", "critical"}:
            flash("Provide an alert title, message and valid severity.", "error")
        else:
            alert = SafetyAlert(title=title[:160], message=message[:3000], location=(request.form.get("location") or "").strip()[:180] or None, severity=severity, issued_by_id=current_user.id)
            db.session.add(alert); db.session.flush(); record("alert_published", alert); db.session.commit()
            flash("Safety alert published.", "success"); return redirect(url_for("main.alerts"))
    return render_template("alert_form.html")
