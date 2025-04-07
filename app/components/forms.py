import streamlit as st
import datetime
import json
import os
from pathlib import Path

from app.utils.database import add_job, log_study_time
from app.utils.file_handler import save_resume, save_cover_letter


# Load configuration
def get_config():
    config_path = Path(__file__).parents[2] / 'config' / 'app_config.json'
    if config_path.exists():
        with open(config_path, 'r') as f:
            return json.load(f)
    else:
        # Default configuration
        return {
            "job_tracking": {
                "statuses": [
                    "Applied",
                    "No Response",
                    "Rejected",
                    "Screening Call",
                    "Interview",
                    "Second Interview",
                    "Final Interview",
                    "Offer",
                    "Accepted",
                    "Declined"
                ]
            },
            "study_tracking": {
                "daily_target_minutes": 70
            }
        }


config = get_config()


def job_application_form():
    """
    Render the form for adding a new job application.

    Returns:
        bool: True if a new application was added, False otherwise
    """
    with st.form("new_job_form"):
        st.subheader("Add New Job Application")

        # Basic job information
        company = st.text_input("Company Name")
        position = st.text_input("Position")
        date_applied = st.date_input("Date Applied", datetime.datetime.now())

        # Status selection
        status_options = config.get('job_tracking', {}).get('statuses', [
            "Applied", "No Response", "Rejected", "Screening Call",
            "Interview", "Second Interview", "Final Interview",
            "Offer", "Accepted", "Declined"
        ])
        status = st.selectbox("Status", status_options)

        # Notes
        notes = st.text_area("Notes (Application details, contacts, etc.)")

        # File uploads
        col1, col2 = st.columns(2)

        with col1:
            resume_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "doc"])

        with col2:
            cover_letter_file = st.file_uploader("Upload Cover Letter", type=["pdf", "docx", "doc"])

        # Submit button
        submitted = st.form_submit_button("Add Job Application")

        # Process form submission
        if submitted:
            if not company or not position:
                st.error("Company name and position are required!")
                return False

            # Save uploaded files
            resume_path = save_resume(resume_file, company, position) if resume_file else None
            cover_letter_path = save_cover_letter(cover_letter_file, company, position) if cover_letter_file else None

            # Add to database
            add_job(
                company=company,
                position=position,
                date_applied=date_applied,
                status=status,
                notes=notes,
                resume_path=resume_path,
                cover_letter_path=cover_letter_path
            )

            st.success(f"Added job application for {position} at {company}!")
            return True

        return False


def study_log_form():
    """
    Render the form for logging study time.

    Returns:
        bool: True if study time was logged, False otherwise
    """
    # Import the dynamic calculation function
    from app.utils.helpers import calculate_daily_target, get_config

    with st.form("study_log_form"):
        st.subheader("Log Your Study Time")

        # Study date selection
        study_date = st.date_input("Date", datetime.datetime.now())

        # Time input in hours and minutes
        col1, col2 = st.columns(2)
        with col1:
            hours = st.number_input("Hours", min_value=0, max_value=24, step=1)
        with col2:
            minutes = st.number_input("Minutes", min_value=0, max_value=59, step=5)

        # Calculate total minutes
        total_minutes = hours * 60 + minutes

        # Get configuration
        config = get_config()

        # Get any manual override from settings
        manual_override = config.get('study_tracking', {}).get('daily_target_minutes', 0)

        # Use either the manual override (if greater than 0) or calculate dynamically
        if manual_override > 0:
            daily_target = manual_override
            target_method = "manually set"
        else:
            total_target_hours = config.get('study_tracking', {}).get('total_target_hours', 300)
            daily_target = calculate_daily_target(total_target_hours)
            target_method = "dynamically calculated"

        # Display target
        target_hours = daily_target // 60
        target_minutes = daily_target % 60

        st.info(f"Daily target: {target_hours}h {target_minutes}m ({target_method})")

        # Progress indication
        if total_minutes > 0:
            progress = min(total_minutes / daily_target, 1)
            progress_percent = int(progress * 100)

            # Display progress bar
            st.progress(progress)

            # Show message based on progress
            if progress >= 1:
                st.success(f"Great job! You've reached {progress_percent}% of your daily target.")
            elif progress >= 0.7:
                st.info(f"Almost there! You're at {progress_percent}% of your daily target.")
            else:
                st.warning(f"You're at {progress_percent}% of your daily target.")

        # Study notes
        notes = st.text_area("Study Notes (topics covered, exercises completed, etc.)")

        # Submit button
        submitted = st.form_submit_button("Log Study Time")

        # Process form submission
        if submitted:
            if total_minutes <= 0:
                st.error("Please enter a study time greater than 0 minutes.")
                return False

            # Log study time
            log_study_time(study_date, total_minutes, notes)

            st.success(f"Logged {hours}h {minutes}m of study time!")
            return True

        return False