import sqlite3
from utils import hash_password 


class User:
    def __init__(self, username, password, email, role):
        self.username = username
        self.password = password
        self.email = email
        self.role = role

    @staticmethod
    def get_user(username, password):
        conn = sqlite3.connect("user.db")
        cursor = conn.cursor()

        hashed_password = hash_password(password)
        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, hashed_password),
        )
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            return User(user_data[1], user_data[2], user_data[3], user_data[4])
        else:
            return None

    @staticmethod
    def register_user(username, password, email):
        conn = sqlite3.connect("user.db")
        cursor = conn.cursor()

        try:
            hashed_password = hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
                (username, hashed_password, email, "user"),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError("Username already exists")
        finally:
            conn.close()
