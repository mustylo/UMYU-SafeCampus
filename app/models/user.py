# Wannan file yana ɗauke da User model na UMYU SafeCampus.
# User model = tsarin da SQLAlchemy zai yi amfani da shi
# wajen ƙirƙirar "users" table a PostgreSQL.

from datetime import datetime, timezone

from app.extensions import db


class User(db.Model):
    # Sunan table da zai kasance a PostgreSQL.
    __tablename__ = "users"

    # Primary Key: yana ba kowane user ID na musamman.
    id = db.Column(db.Integer, primary_key=True)

    # Cikakken sunan mai amfani.
    # nullable=False yana nufin ba za a bar wannan filin empty ba.
    full_name = db.Column(db.String(120), nullable=False)

    # Email dole ne ya zama na musamman.
    # unique=True yana hana users biyu amfani da email ɗaya.
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)

    # Lambar waya; za mu iya barin ta empty.
    phone = db.Column(db.String(30), nullable=True)

    # Anan za mu adana HASH na password, ba password ɗin kansa ba.
    password_hash = db.Column(db.String(255), nullable=False)

    # Matsayin account.
    # Misali: "active" ko "inactive".
    account_status = db.Column(
        db.String(20),
        nullable=False,
        default="active",
    )

    # Lokacin da aka ƙirƙiri account.
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    # Lokacin da aka sabunta account.
    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        # Wannan yana taimakawa wajen ganin user cikin sauƙi
        # idan muna debugging.
        return f"<User {self.email}>"
