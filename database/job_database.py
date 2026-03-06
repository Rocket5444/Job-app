# SQLite database helper module for storing job application records.
#
# This module replaces JSON-based tracking with a small local database.
# It is beginner-friendly and uses Python's built-in sqlite3 package.

import sqlite3
from datetime import datetime


# Name of the SQLite database file created in the project directory.
DB_FILE = "job_applications.db"


# Create DB + applications table if they do not already exist.
def initialize_database():
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company TEXT,
                    title TEXT,
                    url TEXT UNIQUE,
                    status TEXT,
                    applied_date TEXT
                )
                """
            )
            conn.commit()
    except sqlite3.Error as exc:
        print(f"Database error during initialization: {exc}")


# Insert one application record into the database.
# If URL already exists (UNIQUE), insertion is skipped safely.
def insert_application(company, title, url, status):
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO applications (company, title, url, status, applied_date)
                VALUES (?, ?, ?, ?, ?)
                """,
                (company, title, url, status, datetime.utcnow().isoformat()),
            )
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        # Happens when URL already exists because url is UNIQUE.
        return False
    except sqlite3.Error as exc:
        print(f"Database error during insert: {exc}")
        return False


# Check if a job URL already exists in the applications table.
def check_if_applied(url):
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM applications WHERE url = ? LIMIT 1", (url,))
            row = cursor.fetchone()
            return row is not None
    except sqlite3.Error as exc:
        print(f"Database error during lookup: {exc}")
        return False


# Return all stored application rows as tuples.
def get_all_applications():
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, company, title, url, status, applied_date
                FROM applications
                ORDER BY id DESC
                """
            )
            return cursor.fetchall()
    except sqlite3.Error as exc:
        print(f"Database error during fetch: {exc}")
        return []
