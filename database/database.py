import datetime
import sqlite3
from utils import hash_password

class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def create_table_users(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                email TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """)
        self.connection.commit()
        self.insert_default_admin()

    def insert_default_admin(self):
        admin_username = "admin"
        admin_password = "admin123"
        admin_email = "admin@example.com"

        self.cursor.execute("SELECT * FROM users WHERE username = ?", (admin_username,))
        if not self.cursor.fetchone():
            hashed_password = hash_password(admin_password)
            self.cursor.execute(
                "INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
                (admin_username, hashed_password, admin_email, "admin")
            )
            self.connection.commit()

    def insert_user(self, username, password, email):
        hashed_password = hash_password(password)
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
                (username, hashed_password, email, "user"),
            )
            self.connection.commit()
        except sqlite3.IntegrityError:
            raise ValueError("Username already exists")

    def fetch_user(self, username, password):
        hashed_password = hash_password(password)
        self.cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, hashed_password),
        )
        return self.cursor.fetchone()

    def fetch_user_role(self, username):
        self.cursor.execute("SELECT role FROM users WHERE username = ?", (username,))
        return self.cursor.fetchone()

    def close(self):
        self.connection.close()

    def create_table_tickets(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tickets(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                price REAL,
                departure_date TEXT NOT NULL,
                arrival_date TEXT NOT NULL,
                departure_time TEXT NOT NULL,
                arrival_time TEXT NOT NULL,
                description TEXT NOT NULL,
                departure_city TEXT NOT NULL,
                arrival_city TEXT NOT NULL,
                photo TEXT
            )
            """
        )
        self.connection.commit()

    def insert_ticket(self, price, departure_date, arrival_date, departure_time, arrival_time, description, departure_city, arrival_city , photo):
        self.cursor.execute(
            """
            INSERT INTO tickets (price, departure_date, arrival_date, departure_time, arrival_time, description, departure_city, arrival_city, photo) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (price, departure_date, arrival_date, departure_time, arrival_time, description, departure_city, arrival_city, photo)
        )
        self.connection.commit()

    def update_visit_count_by_day(self):
        conn = sqlite3.connect("visits.db")
        cursor = conn.cursor()

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS visits (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            day TEXT,
                            visit_count INTEGER)"""
        )

        current_day = datetime.datetime.today().strftime("%a")

        cursor.execute("SELECT visit_count FROM visits WHERE day = ?", (current_day,))
        result = cursor.fetchone()

        if result:
            visit_count = result[0] + 1
            cursor.execute(
                "UPDATE visits SET visit_count = ? WHERE day = ?",
                (visit_count, current_day),
            )
        else:
            visit_count = 1
            cursor.execute(
                "INSERT INTO visits (day, visit_count) VALUES (?, ?)",
                (current_day, visit_count),
            )

        conn.commit()
        conn.close()

    def reset_weekly_data(self):
        if datetime.datetime.now().strftime("%a") == "Sun":
            conn = sqlite3.connect("visits.db")
            cursor = conn.cursor()

            cursor.execute("DELETE FROM visits")

            conn.commit()
            conn.close()
            print("Weekly data reset.")
