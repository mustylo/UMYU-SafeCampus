
import os

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate

from app.extensions import db

# Load environment variables from .env.
load_dotenv()

# Initialize Flask-Migrate.
migrate = Migrate()


def create_app(test_config=None):
    """Create and configure the UMYU SafeCampus application."""

    app = Flask(__name__)

    # Application configuration.
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY"),
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
    )

    # Allow separate configuration for automated tests.
    if test_config:
        app.config.update(test_config)

    # Stop early if required configuration is missing.
    if not app.config.get("SECRET_KEY"):
        raise RuntimeError(
            "SECRET_KEY is missing. Add it to your .env file."
        )

    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        raise RuntimeError(
            "DATABASE_URL is missing. Check your .env file."
        )

    # Initialize database and migration extensions.
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models so SQLAlchemy and Alembic can discover them.
    from app.models import User
    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    # Temporary homepage until we build the real website.
    @app.get("/")
    def home():
        return "UMYU SafeCampus is running!"

    return app
