import sqlite3
from pathlib import Path


# Absolute database location:
# intelligent-energy-analytics-main/energy_data.db
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "energy_data.db"


def get_connection():
    connection = sqlite3.connect(str(DB_PATH))
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS measurements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                voltage REAL NOT NULL,
                current REAL NOT NULL,
                active_power REAL NOT NULL,
                reactive_power REAL NOT NULL,
                power_factor REAL NOT NULL,
                frequency REAL NOT NULL
            )
            """
        )
        connection.commit()


def save_measurement(data):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO measurements (
                timestamp,
                voltage,
                current,
                active_power,
                reactive_power,
                power_factor,
                frequency
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data["timestamp"],
                data["voltage"],
                data["current"],
                data["active_power"],
                data["reactive_power"],
                data["power_factor"],
                data["frequency"],
            ),
        )

        connection.commit()
        return cursor.lastrowid


def load_measurements():
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                id,
                timestamp,
                voltage,
                current,
                active_power,
                reactive_power,
                power_factor,
                frequency
            FROM measurements
            ORDER BY id ASC
            """
        ).fetchall()

    return [dict(row) for row in rows]