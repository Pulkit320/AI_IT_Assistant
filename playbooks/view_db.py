"""
Database Viewer Utility Script.
Prints all database tables and records formatted in the terminal.
"""

import sqlite3
import os

DB_PATH = "helpdesk.db"


def view_database():
    """Queries SQLite database and displays formatted table contents."""
    if not os.path.exists(DB_PATH):
        print(f"Database file '{DB_PATH}' not found. Run 'python3 -m backend.database.init_db' first.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall() if not t[0].startswith("sqlite_")]

    print("=" * 80)
    print(" HELPDESK DATABASE VIEWER (helpdesk.db)")
    print("=" * 80)

    for table in tables:
        print(f"\n--- TABLE: {table.upper()} ---")
        cursor.execute(f"PRAGMA table_info({table});")
        columns = [col[1] for col in cursor.fetchall()]
        print(" | ".join(columns))
        print("-" * 80)

        cursor.execute(f"SELECT * FROM {table};")
        rows = cursor.fetchall()
        if not rows:
            print("(No records found)")
        else:
            for row in rows:
                print(" | ".join(str(val) for val in row))

    conn.close()
    print("\n" + "=" * 80)


if __name__ == "__main__":
    view_database()
