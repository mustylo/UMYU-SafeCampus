import os

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_migrate import Migrate
import click

from app.extensions import csrf, db, limiter, login_manager

load_dotenv()
migrate = Migrate()


def create_app(test_config=None):
    """Create the UMYU SafeCampus application without exposing secrets."""
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY"),
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=os.getenv("FLASK_ENV") == "production",
        WTF_CSRF_TIME_LIMIT=3600,
        MAX_CONTENT_LENGTH=5 * 1024 * 1024,
    )
    if test_config:
        app.config.update(test_config)
    if not app.config.get("SECRET_KEY"):
        raise RuntimeError("SECRET_KEY is missing. Add it to your .env file.")
    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        raise RuntimeError("DATABASE_URL is missing. Check your .env file.")

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)
    limiter.init_app(app)

    from app.models import User  # Ensure migration discovery.

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    from app.auth.routes import auth_bp
    from app.main.routes import main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    @app.cli.command("seed-catalog")
    def seed_catalog():
        """Create missing core departments and categories without deleting records."""
        from app.models import CaseCategory, Department
        from app.services.catalog import CATEGORIES, DEPARTMENTS
        departments = {}
        for code, (name, description) in DEPARTMENTS.items():
            department = Department.query.filter_by(code=code).first()
            if not department:
                department = Department(code=code, name=name, description=description)
                db.session.add(department)
            departments[code] = department
        db.session.flush()
        for name, slug, code, sensitive in CATEGORIES:
            if not CaseCategory.query.filter_by(slug=slug).first():
                db.session.add(CaseCategory(name=name, slug=slug, department=departments[code], is_health_sensitive=sensitive))
        db.session.commit()
        click.echo("SafeCampus catalog is ready.")

    @app.errorhandler(403)
    def forbidden(_error):
        return render_template("error.html", code=403, message="You do not have permission to access that resource."), 403

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("error.html", code=404, message="The page you requested was not found."), 404

    return app
