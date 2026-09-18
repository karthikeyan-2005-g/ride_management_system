import sqlite3
import os


# =====================================================
# DATABASE CONFIGURATION
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE = os.path.join(
    BASE_DIR,
    "rental_cars.db"
)


# =====================================================
# DATABASE CONNECTION
# =====================================================

def get_db_connection():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    # Enable foreign key support
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


# =====================================================
# INITIALIZE DATABASE
# =====================================================

def init_db():

    conn = get_db_connection()

    cursor = conn.cursor()


    # =================================================
    # USERS TABLE
    # =================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL

        )
    """)


    # =================================================
    # CARS TABLE
    # =================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cars (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            brand TEXT NOT NULL,

            model TEXT NOT NULL,

            type TEXT NOT NULL,

            seats INTEGER NOT NULL,

            transmission TEXT NOT NULL,

            price_per_day REAL NOT NULL,

            image TEXT,

            available INTEGER DEFAULT 1

        )
    """)


    # =================================================
    # BOOKINGS TABLE
    # =================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        car_id INTEGER NOT NULL,
        customer_name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        pickup_location TEXT NOT NULL,
        pickup_date TEXT NOT NULL,
        return_date TEXT NOT NULL,
        total_price REAL NOT NULL,
        status TEXT DEFAULT 'Confirmed',
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (car_id) REFERENCES cars(id)
    )
""")


    # =================================================
    # CHECK CARS
    # =================================================

    cursor.execute(
        "SELECT COUNT(*) FROM cars"
    )

    count = cursor.fetchone()[0]


    # =================================================
    # ADD SAMPLE CARS
    # =================================================

    if count == 0:

        cars = [

            (
                "Toyota Camry",
                "Toyota",
                "Camry",
                "sedan",
                5,
                "Automatic",
                2500,
                "https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?auto=format&fit=crop&w=800&q=80",
                1
            ),

            (
                "Hyundai Creta",
                "Hyundai",
                "Creta",
                "suv",
                5,
                "Automatic",
                2200,
                "https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?auto=format&fit=crop&w=800&q=80",
                1
            ),

            (
                "Maruti Swift",
                "Maruti",
                "Swift",
                "hatchback",
                5,
                "Manual",
                1500,
                "https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?auto=format&fit=crop&w=800&q=80",
                1
            ),

            (
                "Toyota Fortuner",
                "Toyota",
                "Fortuner",
                "suv",
                7,
                "Automatic",
                4000,
                "https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?auto=format&fit=crop&w=800&q=80",
                1
            ),

            (
                "BMW 3 Series",
                "BMW",
                "3 Series",
                "luxury",
                5,
                "Automatic",
                5000,
                "https://images.unsplash.com/photo-1555215695-3004980ad54e?auto=format&fit=crop&w=800&q=80",
                1
            ),

            (
                "Honda City",
                "Honda",
                "City",
                "sedan",
                5,
                "Automatic",
                2000,
                "https://images.unsplash.com/photo-1590362891991-f776e747a588?auto=format&fit=crop&w=800&q=80",
                1
            ),

            (
                "Kia Seltos",
                "Kia",
                "Seltos",
                "suv",
                5,
                "Automatic",
                2300,
                "https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?auto=format&fit=crop&w=800&q=80",
                1
            )
        ]


        # =================================================
        # INSERT CARS
        # =================================================

        cursor.executemany("""
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
        """, cars)


    # =================================================
    # SAVE CHANGES
    # =================================================

    conn.commit()

    conn.close()


# =====================================================
# RUN DATABASE INITIALIZATION
# =====================================================

if __name__ == "__main__":

    init_db()

    print("===================================")
    print("Database initialized successfully!")
    print("Database:", DATABASE)
    print("===================================")