from database import db


# =========================
# USER MODEL
# =========================

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )


# =========================
# CAR MODEL
# =========================

class Car(db.Model):

    __tablename__ = "cars"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    brand = db.Column(
        db.String(100),
        nullable=False
    )

    model = db.Column(
        db.String(100),
        nullable=False
    )

    type = db.Column(
        db.String(50),
        nullable=False
    )

    seats = db.Column(
        db.Integer,
        nullable=False
    )

    transmission = db.Column(
        db.String(50),
        nullable=False
    )

    price_per_day = db.Column(
        db.Float,
        nullable=False
    )

    image = db.Column(
        db.String(500)
    )

    available = db.Column(
        db.Boolean,
        default=True
    )


# =========================
# BOOKING MODEL
# =========================

class Booking(db.Model):

    __tablename__ = "bookings"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    car_id = db.Column(
        db.Integer,
        db.ForeignKey("cars.id"),
        nullable=False
    )

    start_date = db.Column(
        db.String(20),
        nullable=False
    )

    end_date = db.Column(
        db.String(20),
        nullable=False
    )

    total_price = db.Column(
        db.Float,
        nullable=False
    )

    status = db.Column(
        db.String(30),
        default="Confirmed"
    )