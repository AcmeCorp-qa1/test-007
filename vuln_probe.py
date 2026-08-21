import sqlite3

def get_user(user_id):
    conn = sqlite3.connect('database.db')
    query = "SELECT * FROM users WHERE id = ?"
    return conn.execute(query, (user_id,)).fetchone()
