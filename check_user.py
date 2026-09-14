from database import get_db_connection

conn = get_db_connection()

users = conn.execute("""
    SELECT id, name, email, password
    FROM users
""").fetchall()

print("\n===== REGISTERED USERS =====")

for user in users:
    print("ID       :", user["id"])
    print("Name     :", user["name"])
    print("Email    :", user["email"])
    print("Password :", user["password"])
    print("----------------------------")

conn.close()