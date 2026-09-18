import sqlite3

conn = sqlite3.connect("rental_cars.db")

cursor = conn.cursor()

columns = [
    ("customer_name", "TEXT"),
    ("email", "TEXT"),
    ("phone", "TEXT"),
    ("pickup_location", "TEXT")
]

for column_name, column_type in columns:

    try:

        cursor.execute(
            f"ALTER TABLE bookings ADD COLUMN {column_name} {column_type}"
        )

        print(f"Added column: {column_name}")

    except sqlite3.OperationalError:

        print(f"Column already exists: {column_name}")


conn.commit()
conn.close()

print("Database update completed successfully!")