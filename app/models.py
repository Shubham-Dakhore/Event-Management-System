from flask_login import UserMixin
from . import db


# ---------------- USER MODEL ----------------
class User(UserMixin, db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(150), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    # Relationship
    bookings = db.relationship(
        "Booking",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.email}>"



# ---------------- BOOKING MODEL ----------------
class Booking(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    phone = db.Column(db.String(15), nullable=False)

    event_type = db.Column(db.String(100), nullable=False)

    event_date = db.Column(db.String(50), nullable=False)   # NEW
    plan = db.Column(db.String(50), nullable=False)         # NEW

    amount = db.Column(db.String(50), nullable=False)

    profile_pic = db.Column(
        db.String(200),
        default="default.png"
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )

    def __repr__(self):
        return f"<Booking {self.event_type}>"