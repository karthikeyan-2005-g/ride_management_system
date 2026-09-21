from flask import Flask, jsonify, request
from flask_cors import CORS

from database import get_db_connection, init_db


# ==========================================
# CREATE FLASK APP
# ==========================================

app = Flask(__name__)

CORS(app)


# ==========================================
# INITIALIZE DATABASE
# ==========================================

init_db()


# ==========================================
# HOME / TEST
# ==========================================

@app.route("/")
def home():

    return jsonify({
        "message": "Rental Car Management System API is running",
        "status": "success"
    })


# ==========================================
# GET ALL CARS
# ==========================================

@app.route("/api/cars", methods=["GET"])
def get_cars():

    conn = get_db_connection()

    cars = conn.execute("""
        SELECT *
        FROM cars
        ORDER BY id
    """).fetchall()

    conn.close()

    return jsonify([
        dict(car)
        for car in cars
    ])


# ==========================================
# GET SINGLE CAR
# ==========================================

@app.route("/api/cars/<int:car_id>", methods=["GET"])
def get_car(car_id):

    conn = get_db_connection()

    car = conn.execute("""
        SELECT *
        FROM cars
        WHERE id = ?
    """, (car_id,)).fetchone()

    conn.close()

    if car is None:

        return jsonify({
            "message": "Car not found"
        }), 404

    return jsonify(dict(car))


# ==========================================
# ADD NEW CAR
# ==========================================

@app.route("/api/cars", methods=["POST"])
def add_car():

    data = request.get_json()

    if not data:

        return jsonify({
            "message": "No data received"
        }), 400

    required_fields = [
        "name",
        "brand",
        "model",
        "type",
        "seats",
        "transmission",
        "price_per_day",
        "image"
    ]

    for field in required_fields:

        if field not in data:

            return jsonify({
                "message": f"{field} is required"
            }), 400


    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO cars
        (
            name,
            brand,
            model,
            type,
            seats,
            transmission,
            price_per_day,
            image,
            available
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["name"],
        data["brand"],
        data["model"],
        data["type"],
        data["seats"],
        data["transmission"],
        data["price_per_day"],
        data["image"],
        data.get("available", 1)
    ))

    conn.commit()

    car_id = cursor.lastrowid

    conn.close()


    return jsonify({
        "message": "Car added successfully",
        "car_id": car_id
    }), 201


# ==========================================
# UPDATE CAR
# ==========================================

@app.route("/api/cars/<int:car_id>", methods=["PUT"])
def update_car(car_id):

    data = request.get_json()

    if not data:

        return jsonify({
            "message": "No data received"
        }), 400


    conn = get_db_connection()

    car = conn.execute("""
        SELECT *
        FROM cars
        WHERE id = ?
    """, (car_id,)).fetchone()

    if car is None:

        conn.close()

        return jsonify({
            "message": "Car not found"
        }), 404


    conn.execute("""
        UPDATE cars
        SET
            name = ?,
            brand = ?,
            model = ?,
            type = ?,
            seats = ?,
            transmission = ?,
            price_per_day = ?,
            image = ?,
            available = ?
        WHERE id = ?
    """, (
        data.get("name", car["name"]),
        data.get("brand", car["brand"]),
        data.get("model", car["model"]),
        data.get("type", car["type"]),
        data.get("seats", car["seats"]),
        data.get("transmission", car["transmission"]),
        data.get("price_per_day", car["price_per_day"]),
        data.get("image", car["image"]),
        data.get("available", car["available"]),
        car_id
    ))

    conn.commit()

    conn.close()


    return jsonify({
        "message": "Car updated successfully"
    })


# ==========================================
# DELETE CAR
# ==========================================

@app.route("/api/cars/<int:car_id>", methods=["DELETE"])
def delete_car(car_id):

    conn = get_db_connection()

    car = conn.execute("""
        SELECT *
        FROM cars
        WHERE id = ?
    """, (car_id,)).fetchone()

    if car is None:

        conn.close()

        return jsonify({
            "message": "Car not found"
        }), 404


    conn.execute("""
        DELETE FROM cars
        WHERE id = ?
    """, (car_id,))

    conn.commit()

    conn.close()


    return jsonify({
        "message": "Car deleted successfully"
    })



# ==========================================
# REGISTER USER
# ==========================================

@app.route("/api/register", methods=["POST"])
def register():

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "No data received"
        }), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({
            "message": "Name, email and password are required"
        }), 400

    conn = get_db_connection()

    # Check existing email
    existing_user = conn.execute(
        "SELECT id FROM users WHERE email = ?",
        (email,)
    ).fetchone()

    if existing_user:
        conn.close()

        return jsonify({
            "message": "Email already registered"
        }), 409

    # Save new user
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (name, email, password)
        VALUES (?, ?, ?)
    """, (
        name,
        email,
        password
    ))

    conn.commit()

    user_id = cursor.lastrowid

    conn.close()

    return jsonify({
        "message": "Registration successful",
        "user": {
            "id": user_id,
            "name": name,
            "email": email
        }
    }), 201



# ==========================================
# USER LOGIN
# ==========================================

@app.route("/api/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "No login data received"
        }), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "message": "Email and password are required"
        }), 400

    conn = get_db_connection()

    user = conn.execute("""
        SELECT id, name, email
        FROM users
        WHERE email = ? AND password = ?
    """, (email, password)).fetchone()

    conn.close()

    if user is None:
        return jsonify({
            "message": "Invalid email or password"
        }), 401

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        }
    }), 200
# ==========================================
# CREATE BOOKING
# ==========================================

@app.route("/api/bookings", methods=["POST"])
def create_booking():

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "No booking data received"
        }), 400


    # ==========================================
    # GET BOOKING DATA
    # ==========================================

    user_id = data.get("user_id")
    car_id = data.get("car_id")

    customer_name = data.get("customer_name")
    email = data.get("email")
    phone = data.get("phone")
    pickup_location = data.get("pickup_location")

    pickup_date = data.get("pickup_date")
    return_date = data.get("return_date")
    total_price = data.get("total_price")


    # ==========================================
    # VALIDATE REQUIRED FIELDS
    # ==========================================

    if not all([
        user_id,
        car_id,
        customer_name,
        email,
        phone,
        pickup_location,
        pickup_date,
        return_date,
        total_price is not None
    ]):

        return jsonify({
            "message": "All booking fields are required"
        }), 400


    # ==========================================
    # DATABASE CONNECTION
    # ==========================================

    conn = get_db_connection()


    # ==========================================
    # CHECK USER
    # ==========================================

    user = conn.execute(
        "SELECT id FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()


    if user is None:

        conn.close()

        return jsonify({
            "message": "User not found"
        }), 404


    # ==========================================
    # CHECK CAR
    # ==========================================

    car = conn.execute(
        "SELECT id, available FROM cars WHERE id = ?",
        (car_id,)
    ).fetchone()


    if car is None:

        conn.close()

        return jsonify({
            "message": "Car not found"
        }), 404


    # ==========================================
    # CHECK CAR AVAILABILITY
    # ==========================================

    if car["available"] == 0:

        conn.close()

        return jsonify({
            "message": "Car is not available"
        }), 400


    # ==========================================
    # INSERT BOOKING
    # ==========================================

    cursor = conn.cursor()


    cursor.execute("""
        INSERT INTO bookings
        (
            user_id,
            car_id,
            customer_name,
            email,
            phone,
            pickup_location,
            pickup_date,
            return_date,
            total_price,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        car_id,
        customer_name,
        email,
        phone,
        pickup_location,
        pickup_date,
        return_date,
        total_price,
        "Confirmed"
    ))


    booking_id = cursor.lastrowid


    # ==========================================
    # SAVE DATABASE
    # ==========================================

    conn.commit()

    conn.close()


    # ==========================================
    # SUCCESS RESPONSE
    # ==========================================

    return jsonify({

        "message": "Booking created successfully",

        "booking_id": booking_id

    }), 201
# ==========================================
# GET USER BOOKINGS
# ==========================================

@app.route("/api/bookings/user/<int:user_id>", methods=["GET"])
def get_user_bookings(user_id):

    conn = get_db_connection()

    bookings = conn.execute("""
        SELECT
            bookings.id,
            bookings.user_id,
            bookings.car_id,
            cars.name AS car_name,
            cars.image,
            bookings.pickup_date,
            bookings.return_date,
            bookings.total_price,
            bookings.status
        FROM bookings
        JOIN cars
            ON bookings.car_id = cars.id
        WHERE bookings.user_id = ?
        ORDER BY bookings.id DESC
    """, (user_id,)).fetchall()

    conn.close()

    return jsonify([
        dict(booking)
        for booking in bookings
    ])


# ==========================================
# CANCEL BOOKING
# ==========================================

@app.route("/api/bookings/<int:booking_id>", methods=["DELETE"])
def cancel_booking(booking_id):

    conn = get_db_connection()

    booking = conn.execute(
        "SELECT car_id FROM bookings WHERE id = ?",
        (booking_id,)
    ).fetchone()

    if booking is None:
        conn.close()
        return jsonify({
            "message": "Booking not found"
        }), 404

    # Make the car available again
    conn.execute(
        "UPDATE cars SET available = 1 WHERE id = ?",
        (booking["car_id"],)
    )

    # Delete the booking
    conn.execute(
        "DELETE FROM bookings WHERE id = ?",
        (booking_id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Booking cancelled successfully"
    }), 200


# ==========================================
# RUN SERVER
# ==========================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )