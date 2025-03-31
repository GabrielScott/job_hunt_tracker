# reset_sections.py
import os
import sys
import sqlite3
from datetime import datetime

# Add the parent directory to sys.path to allow imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from app.utils.database import get_db_connection

# Your custom study sections
CUSTOM_STUDY_SECTIONS = [
    {"id": "section_1", "name": "General Probability", "description": "Basic probability concepts and rules",
     "order": 1},
    {"id": "section_2", "name": "Univariate Distributions",
     "description": "Common distributions like Poisson & Exponential", "order": 2},
    {"id": "section_3", "name": "Multivariate Distributions",
     "description": "Conditional and marginal probabily functions", "order": 3},
    {"id": "section_4", "name": "Insurance and Risk Management",
     "description": "Basic insurance mechanics like deductibles, policy limits, and coinsurance.", "order": 4},
    {"id": "section_5", "name": "Review Section", "description": "Summary of all sections", "order": 5},
]


def reset_study_sections():
    """Reset the study sections in the database to match the custom ones."""
    conn = get_db_connection()
    c = conn.cursor()

    try:
        # Delete existing section achievements first
        c.execute("DELETE FROM achievements WHERE type = 'SECTION'")

        # Then delete all study sections
        c.execute("DELETE FROM study_sections")

        # Insert the custom sections
        for section in CUSTOM_STUDY_SECTIONS:
            c.execute(
                "INSERT INTO study_sections (id, name, description, order_num, completed) VALUES (?, ?, ?, ?, 0)",
                (section['id'], section['name'], section['description'], section['order'])
            )

            # Create an achievement for each section
            section_achievement_id = f"complete_{section['id']}"
            c.execute(
                "INSERT INTO achievements (id, type, name, description, threshold, icon) VALUES (?, ?, ?, ?, ?, ?)",
                (section_achievement_id, "SECTION", f"Mastered: {section['name']}",
                 f"Complete the {section['name']} section of the study manual", 1, "📚")
            )

        conn.commit()
        print("Study sections have been reset successfully!")

    except Exception as e:
        conn.rollback()
        print(f"Error resetting study sections: {str(e)}")
    finally:
        conn.close()


if __name__ == "__main__":
    reset_study_sections()