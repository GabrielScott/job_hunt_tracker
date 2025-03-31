# app/utils/achievements.py

import sqlite3
from datetime import datetime
from pathlib import Path
import json
import pandas as pd

from app.utils.database import get_db_connection, get_study_logs

# Achievement types
ACHIEVEMENT_TYPES = {
    "STUDY_TIME": "Total study time milestone",
    "STREAK": "Consecutive study days",
    "SECTION": "Study manual section completion"
}

# Predefined achievements
DEFAULT_ACHIEVEMENTS = [
    # Study time achievements (hours)
    {"id": "time_30", "type": "STUDY_TIME", "name": "Getting Started",
     "description": "Complete 30 hours of study time (10% of exam preparation)", "threshold": 30 * 60, "icon": "🌱"},
    {"id": "time_75", "type": "STUDY_TIME", "name": "Quarter Way There",
     "description": "Complete 75 hours of study time (25% of exam preparation)", "threshold": 75 * 60, "icon": "🌿"},
    {"id": "time_150", "type": "STUDY_TIME", "name": "Halfway Point",
     "description": "Complete 150 hours of study time (50% of exam preparation)", "threshold": 150 * 60, "icon": "🌳"},
    {"id": "time_225", "type": "STUDY_TIME", "name": "Final Stretch",
     "description": "Complete 225 hours of study time (75% of exam preparation)", "threshold": 225 * 60, "icon": "🌲"},
    {"id": "time_300", "type": "STUDY_TIME", "name": "Fully Prepared!",
     "description": "Complete all 300 hours of recommended study time", "threshold": 300 * 60, "icon": "🎓"},

    # Streak achievements
    {"id": "streak_3", "type": "STREAK", "name": "Consistency Begins", "description": "Study 3 days in a row",
     "threshold": 3, "icon": "🔥"},
    {"id": "streak_7", "type": "STREAK", "name": "Solid Week", "description": "Study 7 days in a row (full week)",
     "threshold": 7, "icon": "🔥🔥"},
    {"id": "streak_14", "type": "STREAK", "name": "Two Week Marathon",
     "description": "Study 14 days in a row (two weeks)", "threshold": 14, "icon": "🔥🔥🔥"},
    {"id": "streak_30", "type": "STREAK", "name": "Monthly Dedication",
     "description": "Study 30 days in a row (one month)", "threshold": 30, "icon": "🔥🔥🔥🔥"},

    # These are placeholders - section achievements will be created dynamically based on manual sections
    {"id": "section_placeholder", "type": "SECTION", "name": "Section Completed",
     "description": "Complete a section of the study manual", "threshold": 1, "icon": "📚"}
]

# Default SOA Exam P study manual sections
DEFAULT_STUDY_SECTIONS = [
    {"id": "section_1", "name": "General Probability", "description": "Basic probability concepts and rules",
     "order": 1},
    {"id": "section_2", "name": "Univariate Distributions", "description": "Common distributions like Poisson & Exponential",
     "order": 2},
    {"id": "section_3", "name": "Multivariate Distributions", "description": "Conditional and marginal probabily functions",
     "order": 3},
    {"id": "section_4", "name": "Insurance and Risk Management",
     "description": "Basic insurance mechanics like deductibles, policy limits, and coinsurance.", "order": 4},
    {"id": "section_5", "name": "Review Section", "description": "Summary of all sections", "order": 5},
]


def init_achievements_db():
    """Initialize the database tables for achievements if they don't exist."""
    conn = get_db_connection()
    c = conn.cursor()

    # Create achievements table to store predefined achievements
    c.execute('''
    CREATE TABLE IF NOT EXISTS achievements (
        id TEXT PRIMARY KEY,
        type TEXT,
        name TEXT,
        description TEXT,
        threshold INTEGER,
        icon TEXT
    )
    ''')

    # Create user_achievements table to track unlocked achievements
    c.execute('''
    CREATE TABLE IF NOT EXISTS user_achievements (
        achievement_id TEXT,
        date_unlocked TEXT,
        PRIMARY KEY (achievement_id),
        FOREIGN KEY (achievement_id) REFERENCES achievements(id)
    )
    ''')

    # Create study_sections table to track sections of the study manual
    c.execute('''
    CREATE TABLE IF NOT EXISTS study_sections (
        id TEXT PRIMARY KEY,
        name TEXT,
        description TEXT,
        completed INTEGER DEFAULT 0,
        date_completed TEXT,
        order_num INTEGER
    )
    ''')

    # Insert default achievements if they don't exist
    for achievement in DEFAULT_ACHIEVEMENTS:
        if achievement['id'] != "section_placeholder":  # Skip the placeholder
            c.execute(
                "INSERT OR IGNORE INTO achievements (id, type, name, description, threshold, icon) VALUES (?, ?, ?, ?, ?, ?)",
                (achievement['id'], achievement['type'], achievement['name'], achievement['description'],
                 achievement['threshold'], achievement['icon'])
            )

    # Insert default study sections if they don't exist
    for section in DEFAULT_STUDY_SECTIONS:
        c.execute(
            "INSERT OR IGNORE INTO study_sections (id, name, description, order_num) VALUES (?, ?, ?, ?)",
            (section['id'], section['name'], section['description'], section['order'])
        )

        # Create an achievement for each section
        section_achievement_id = f"complete_{section['id']}"
        c.execute(
            "INSERT OR IGNORE INTO achievements (id, type, name, description, threshold, icon) VALUES (?, ?, ?, ?, ?, ?)",
            (section_achievement_id, "SECTION", f"Mastered: {section['name']}",
             f"Complete the {section['name']} section of the study manual", 1, "📚")
        )

    conn.commit()
    conn.close()


def get_all_achievements():
    """Get all achievements with their unlock status."""
    conn = get_db_connection()

    # Get all achievements with unlocked status
    achievements_df = pd.read_sql('''
    SELECT a.id, a.type, a.name, a.description, a.threshold, a.icon, 
           ua.date_unlocked, 
           CASE WHEN ua.date_unlocked IS NULL THEN 0 ELSE 1 END as unlocked
    FROM achievements a
    LEFT JOIN user_achievements ua ON a.id = ua.achievement_id
    ORDER BY a.type, a.threshold
    ''', conn)

    conn.close()
    return achievements_df


def get_unlocked_achievements():
    """Get only unlocked achievements."""
    conn = get_db_connection()

    unlocked_df = pd.read_sql('''
    SELECT a.id, a.type, a.name, a.description, a.threshold, a.icon, ua.date_unlocked
    FROM achievements a
    JOIN user_achievements ua ON a.id = ua.achievement_id
    ORDER BY ua.date_unlocked DESC
    ''', conn)

    conn.close()
    return unlocked_df


def unlock_achievement(achievement_id):
    """Mark an achievement as unlocked."""
    conn = get_db_connection()
    c = conn.cursor()

    # Check if already unlocked
    c.execute("SELECT achievement_id FROM user_achievements WHERE achievement_id = ?", (achievement_id,))
    if c.fetchone() is None:
        # Not unlocked yet, so unlock it
        c.execute(
            "INSERT INTO user_achievements (achievement_id, date_unlocked) VALUES (?, ?)",
            (achievement_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()
        conn.close()
        return True  # Newly unlocked

    conn.close()
    return False  # Already unlocked


def get_study_sections():
    """Get all study sections with completion status."""
    conn = get_db_connection()

    sections_df = pd.read_sql('''
    SELECT id, name, description, completed, date_completed, order_num
    FROM study_sections
    ORDER BY order_num
    ''', conn)

    conn.close()
    return sections_df


def mark_section_completed(section_id):
    """Mark a study section as completed."""
    conn = get_db_connection()
    c = conn.cursor()

    # Mark section as completed
    c.execute(
        "UPDATE study_sections SET completed = 1, date_completed = ? WHERE id = ?",
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), section_id)
    )

    # Unlock the corresponding achievement
    achievement_id = f"complete_{section_id}"
    unlock_achievement(achievement_id)

    conn.commit()
    conn.close()


def mark_section_incomplete(section_id):
    """Mark a study section as not completed."""
    conn = get_db_connection()
    c = conn.cursor()

    c.execute(
        "UPDATE study_sections SET completed = 0, date_completed = NULL WHERE id = ?",
        (section_id,)
    )

    conn.commit()
    conn.close()


def check_for_achievements():
    """
    Check for new achievements based on current progress.
    Returns a list of newly unlocked achievements.
    """
    newly_unlocked = []

    # Get study data
    study_df = get_study_logs()

    if study_df.empty:
        return newly_unlocked

    # Check for time-based achievements
    total_minutes = study_df['duration'].sum()
    time_achievements = pd.read_sql(
        "SELECT id, threshold FROM achievements WHERE type = 'STUDY_TIME' AND id NOT IN (SELECT achievement_id FROM user_achievements)",
        get_db_connection()
    )

    for _, achievement in time_achievements.iterrows():
        if total_minutes >= achievement['threshold']:
            if unlock_achievement(achievement['id']):
                newly_unlocked.append(achievement['id'])

    # Check for streak achievements
    from app.components.metrics import calculate_streak
    current_streak = calculate_streak(study_df)

    streak_achievements = pd.read_sql(
        "SELECT id, threshold FROM achievements WHERE type = 'STREAK' AND id NOT IN (SELECT achievement_id FROM user_achievements)",
        get_db_connection()
    )

    for _, achievement in streak_achievements.iterrows():
        if current_streak >= achievement['threshold']:
            if unlock_achievement(achievement['id']):
                newly_unlocked.append(achievement['id'])

    return newly_unlocked


def get_achievement_by_id(achievement_id):
    """Get details for a specific achievement."""
    conn = get_db_connection()

    achievement_df = pd.read_sql(
        "SELECT id, type, name, description, threshold, icon FROM achievements WHERE id = ?",
        conn,
        params=(achievement_id,)
    )

    conn.close()

    if not achievement_df.empty:
        return achievement_df.iloc[0].to_dict()

    return None