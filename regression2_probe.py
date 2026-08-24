import sqlite3

def get_user(user_id):
    conn = sqlite3.connect('database.db')
    query = f"SELECT * FROM users WHERE user_id = {user_id}"
    return conn.execute(query).fetchone()
