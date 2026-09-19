"""
database.py
Handles SQLite connection and idempotent schema creation for Hospital AI.
"""

import sqlite3
import os

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "hospital.db")


def get_connection():
    """Return a SQLite connection with row access by column name."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_database():
    """Create all required tables if they do not already exist."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            patient_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            department TEXT NOT NULL,
            priority TEXT NOT NULL,
            admission_status TEXT NOT NULL,
            assigned_bed TEXT,
            current_stage TEXT NOT NULL,
            admission_date TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS beds (
            ward TEXT PRIMARY KEY,
            total_beds INTEGER NOT NULL,
            occupied_beds INTEGER NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS emergency_cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            priority TEXT NOT NULL,
            department TEXT NOT NULL,
            required_resources TEXT NOT NULL,
            waiting_time_min INTEGER NOT NULL,
            assigned_agent TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS lab_tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT,
            patient_name TEXT NOT NULL,
            test_name TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL,
            requested_time TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS imaging_scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT,
            patient_name TEXT NOT NULL,
            scan_type TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL,
            scheduled_time TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS surgeries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            surgery_name TEXT NOT NULL,
            operating_room TEXT NOT NULL,
            surgeon TEXT NOT NULL,
            priority TEXT NOT NULL,
            scheduled_time TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            category TEXT NOT NULL,
            stock_level INTEGER NOT NULL,
            reorder_threshold INTEGER NOT NULL,
            status TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS nursing_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nurse_name TEXT NOT NULL,
            task TEXT NOT NULL,
            patient_name TEXT,
            status TEXT NOT NULL,
            shift TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS blood_inventory (
            blood_type TEXT PRIMARY KEY,
            units_available INTEGER NOT NULL,
            status TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS organ_inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            organ_type TEXT NOT NULL,
            status TEXT NOT NULL,
            match_status TEXT NOT NULL,
            location TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS agent_status (
            agent_name TEXT PRIMARY KEY,
            status TEXT NOT NULL,
            current_task TEXT NOT NULL,
            tasks_completed INTEGER NOT NULL,
            last_activity TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS agent_activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_name TEXT NOT NULL,
            activity TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            priority TEXT NOT NULL,
            situation TEXT NOT NULL,
            agents_consulted TEXT NOT NULL,
            recommendation TEXT NOT NULL,
            human_approval TEXT NOT NULL,
            status TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS screenings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            screening_type TEXT NOT NULL,
            status TEXT NOT NULL,
            result TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS compliance_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            check_type TEXT NOT NULL,
            status TEXT NOT NULL,
            details TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
