import sqlite3
import os
import pandas as pd
import json
from pathlib import Path
from datetime import datetime


# Load configuration
def get_config():
    config_path = Path(__file__).parents[2] / 'config' / 'app_config.json'
    if config_path.exists():
        with open(config_path, 'r') as f:
            return json.load(f)
    else:
        # Default configuration
        return {
            "database": {
                "path": "data/database/job_hunt_tracker.db"
            },
            "uploads": {
                "path": "data/uploads"
            }
        }


config = get_config()

# Ensure we use absolute paths
BASE_DIR = Path(__file__).parents[2]
DB_PATH = BASE_DIR / config['database']['path']
UPLOADS_PATH = BASE_DIR / config['uploads']['path']

# Make sure directories exist
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
UPLOADS_PATH.mkdir(parents=True, exist_ok=True)


def get_db_connection():
    """Create a database connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database with required tables."""
    conn = get_db_connection()
    c = conn.cursor()

    # Create jobs table if it doesn't exist
    c.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY,
        company TEXT,
        position TEXT,
        date_applied DATE,
        status TEXT,
        last_updated DATE,
        notes TEXT,
        resume_path TEXT,
        cover_letter_path TEXT
    )
    ''')

    # Create study_log table if it doesn't exist
    c.execute('''
    CREATE TABLE IF NOT EXISTS study_log (
        id INTEGER PRIMARY KEY,
        date DATE,
        duration INTEGER,
        notes TEXT
    )
    ''')

    conn.commit()
    conn.close()


# Job-related database operations
def add_job(company, position, date_applied, status, notes, resume_path=None, cover_letter_path=None):
    """Add a new job application to the database."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO jobs (company, position, date_applied, status, last_updated, notes, resume_path, cover_letter_path) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (company, position, date_applied, status, datetime.now().date(), notes, resume_path, cover_letter_path)
    )
    conn.commit()
    job_id = c.lastrowid
    conn.close()
    return job_id


def update_job(job_id, status=None, notes=None, resume_path=None, cover_letter_path=None):
    """Update an existing job application."""
    conn = get_db_connection()
    c = conn.cursor()

    # Get current job details
    c.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
    job = c.fetchone()

    if job:
        # Update only the fields that are provided
        status = status if status is not None else job['status']
        notes = notes if notes is not None else job['notes']
        resume_path = resume_path if resume_path is not None else job['resume_path']
        cover_letter_path = cover_letter_path if cover_letter_path is not None else job['cover_letter_path']

        c.execute(
            "UPDATE jobs SET status = ?, notes = ?, last_updated = ?, resume_path = ?, cover_letter_path = ? WHERE id = ?",
            (status, notes, datetime.now().date(), resume_path, cover_letter_path, job_id)
        )
        conn.commit()
        conn.close()
        return True

    conn.close()
    return False


def get_all_jobs():
    """Get all job applications."""
    conn = get_db_connection()
    jobs_df = pd.read_sql("SELECT * FROM jobs ORDER BY date_applied DESC", conn)
    conn.close()
    return jobs_df


def get_job(job_id):
    """Get a specific job application."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
    job = c.fetchone()
    conn.close()
    return dict(job) if job else None


def delete_job(job_id):
    """Delete a job application."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
    conn.commit()
    conn.close()


# Study-related database operations
def log_study_time(date, duration, notes=""):
    """Log study time for a specific date."""
    conn = get_db_connection()
    c = conn.cursor()

    # Check if there's already an entry for this date
    c.execute("SELECT id, duration FROM study_log WHERE date = ?", (date,))
    existing = c.fetchone()

    if existing:
        # Update existing entry
        new_duration = duration
        c.execute(
            "UPDATE study_log SET duration = ?, notes = ? WHERE id = ?",
            (new_duration, notes, existing['id'])
        )
        conn.commit()
        conn.close()
        return existing['id']
    else:
        # Create new entry
        c.execute(
            "INSERT INTO study_log (date, duration, notes) VALUES (?, ?, ?)",
            (date, duration, notes)
        )
        conn.commit()
        log_id = c.lastrowid
        conn.close()
        return log_id


def get_study_logs():
    """Get all study logs."""
    conn = get_db_connection()
    study_df = pd.read_sql("SELECT * FROM study_log ORDER BY date DESC", conn)
    conn.close()
    return study_df


def reset_job_data():
    """Reset all job application data."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM jobs")
    conn.commit()
    conn.close()


def reset_study_data():
    """Reset all study log data."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM study_log")
    conn.commit()
    conn.close()


def reset_all_data():
    """Reset all application data."""
    reset_job_data()
    reset_study_data()