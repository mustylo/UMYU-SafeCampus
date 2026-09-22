import os

from dotenv import load_dotenv
from flask import Flask

from app.extensions import db

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

    db.init_app(app)

    @app.get("/")
    def home():
        return "UMYU SafeCampus is running!"

    return app
