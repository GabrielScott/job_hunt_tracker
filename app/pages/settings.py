# app/pages/settings.py

import streamlit as st
import pandas as pd
import json
import os
from pathlib import Path
from io import BytesIO
from datetime import datetime

from app.utils.database import get_all_jobs, get_study_logs, reset_job_data, reset_study_data, reset_all_data
from app.utils.file_handler import export_dataframe
from app.components.section_manager import display_section_manager, display_reset_button


# Load configuration
def get_config():
    config_path = Path(__file__).parents[2] / 'config' / 'app_config.json'
    if config_path.exists():
        with open(config_path, 'r') as f:
            return json.load(f)
    else:
        # Default configuration
        return {
            "app": {
                "name": "Job Hunt & Study Tracker",
                "version": "1.0.0"
            }
        }


config = get_config()


def show():
    """Display the settings page."""
    # Custom styling for consistent headers
    st.markdown("<h2 style='color: #67597A; border-bottom: 2px solid #E5F77D; padding-bottom: 5px;'>Settings</h2>",
                unsafe_allow_html=True)

    # App information
    st.sidebar.markdown("---")
    app_name = config.get('app', {}).get('name', "Job Hunt & Study Tracker")
    app_version = config.get('app', {}).get('version', "1.0.0")
    st.sidebar.info(f"{app_name} v{app_version}")

    # Create tabs for different settings sections
    tab1, tab2, tab3, tab4 = st.tabs(["Export Data", "Reset Data", "Application Settings", "Study Sections"])

    with tab1:
        show_export_options()

    with tab2:
        show_reset_options()

    with tab3:
        show_app_settings()

    with tab4:
        # Display the study section manager
        display_section_manager()

        # Add section for quick reset to custom sections
        st.markdown("---")
        display_reset_button()


def show_export_options():
    """Display options for exporting data."""
    st.markdown("<h3 style='color: #67597A;'>Export Data</h3>", unsafe_allow_html=True)

    export_format = st.radio("Export Format", ["CSV", "Excel"])

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Export Job Applications"):
            jobs_df = get_all_jobs()

            if not jobs_df.empty:
                filename = "job_applications"
                st.markdown(
                    export_dataframe(jobs_df, filename, export_format.lower()),
                    unsafe_allow_html=True
                )
            else:
                st.info("No job application data to export.")

    with col2:
        if st.button("Export Study Log"):
            study_df = get_study_logs()

            if not study_df.empty:
                filename = "study_log"
                st.markdown(
                    export_dataframe(study_df, filename, export_format.lower()),
                    unsafe_allow_html=True
                )
            else:
                st.info("No study log data to export.")

    # Export all data
    if st.button("Export All Data"):
        jobs_df = get_all_jobs()
        study_df = get_study_logs()

        if not jobs_df.empty or not study_df.empty:
            if export_format.lower() == "csv":
                # For CSV, we'll create separate files
                download_links = []

                if not jobs_df.empty:
                    download_links.append(export_dataframe(jobs_df, "job_applications", "csv"))

                if not study_df.empty:
                    download_links.append(export_dataframe(study_df, "study_log", "csv"))

                for link in download_links:
                    st.markdown(link, unsafe_allow_html=True)
            else:
                # For Excel, we'll create a single file with multiple sheets
                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    if not jobs_df.empty:
                        jobs_df.to_excel(writer, sheet_name='Job Applications', index=False)

                    if not study_df.empty:
                        study_df.to_excel(writer, sheet_name='Study Log', index=False)

                output.seek(0)

                # Create download link
                import base64
                b64 = base64.b64encode(output.read()).decode()
                href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="job_hunt_tracker_data.xlsx">Download Excel File</a>'
                st.markdown(href, unsafe_allow_html=True)
        else:
            st.info("No data to export.")


def show_reset_options():
    """Display options for resetting data."""
    st.markdown("<h3 style='color: #67597A;'>Reset Data</h3>", unsafe_allow_html=True)
    st.warning("Warning: This will delete your data. This action cannot be undone!")

    reset_col1, reset_col2 = st.columns(2)

    with reset_col1:
        if st.button("Reset Job Applications"):
            with st.spinner("Resetting job application data..."):
                reset_job_data()
                st.success("Job application data has been reset!")

    with reset_col2:
        if st.button("Reset Study Log"):
            with st.spinner("Resetting study log data..."):
                reset_study_data()
                st.success("Study log data has been reset!")

    # Add additional confirmation for resetting all data
    st.markdown("<h4 style='color: #67597A;'>Reset All Data</h4>", unsafe_allow_html=True)

    # Create a confirmation check
    confirm_reset = st.checkbox("I understand this will delete ALL my data and cannot be undone.")

    if confirm_reset:
        if st.button("Reset ALL Data"):
            with st.spinner("Resetting all data..."):
                reset_all_data()
                st.success("All data has been reset!")


def show_app_settings():
    """Display application settings."""
    st.markdown("<h3 style='color: #67597A;'>Application Settings</h3>", unsafe_allow_html=True)

    # Load current configuration
    current_config = get_config()

    # Study settings
    st.markdown("<h4 style='color: #67597A;'>Study Settings</h4>", unsafe_allow_html=True)

    # Add test date picker
    default_test_date = current_config.get('study_tracking', {}).get('test_date', "2025-07-16")
    try:
        default_date_obj = datetime.strptime(default_test_date, "%Y-%m-%d").date()
    except:
        default_date_obj = datetime(2025, 7, 16).date()

    test_date = st.date_input(
        "Test Date",
        value=default_date_obj,
        min_value=datetime.now().date(),
        help="The date of your exam - daily targets will be calculated based on this"
    )

    # Show note about dynamic calculation
    st.info(
        "Your daily study target will be calculated automatically based on the remaining time until your test date " +
        "and your remaining study hours."
    )

    # Keep the manual override option but make it clear it's not the primary method
    manual_daily_target = st.number_input(
        "Manual Daily Target Override (minutes)",
        min_value=0,
        max_value=480,
        value=current_config.get('study_tracking', {}).get('daily_target_minutes', 70),
        step=5,
        help="This will override the automatic calculation if non-zero"
    )

    weekly_target_days = st.number_input(
        "Weekly Target Days",
        min_value=1,
        max_value=7,
        value=current_config.get('study_tracking', {}).get('weekly_target_days', 5),
        step=1
    )

    total_target_hours = st.number_input(
        "Total Target Hours (for SOA Exam)",
        min_value=50,
        max_value=1000,
        value=current_config.get('study_tracking', {}).get('total_target_hours', 300),
        step=10
    )

    # [Rest of the settings function remains unchanged]

    # Job application settings
    st.markdown("<h4 style='color: #67597A;'>Job Application Settings</h4>", unsafe_allow_html=True)

    weekly_goal = st.number_input(
        "Weekly Application Goal",
        min_value=1,
        max_value=50,
        value=current_config.get('job_tracking', {}).get('weekly_goal', 5),
        step=1
    )

    # Status options (text area for easier editing)
    default_statuses = "\n".join(current_config.get('job_tracking', {}).get('statuses', [
        "Applied", "No Response", "Rejected", "Screening Call",
        "Interview", "Second Interview", "Final Interview",
        "Offer", "Accepted", "Declined"
    ]))

    status_options = st.text_area(
        "Status Options (one per line)",
        value=default_statuses,
        height=200
    )

    # Save button
    if st.button("Save Settings"):
        try:
            # Parse status options
            statuses = [s.strip() for s in status_options.split('\n') if s.strip()]

            # Update configuration
            current_config['study_tracking'] = {
                'daily_target_minutes': manual_daily_target,
                'weekly_target_days': weekly_target_days,
                'total_target_hours': total_target_hours,
                'test_date': test_date.strftime("%Y-%m-%d")
            }

            current_config['job_tracking'] = {
                'weekly_goal': weekly_goal,
                'statuses': statuses
            }

            # Save configuration
            config_path = Path(__file__).parents[2] / 'config' / 'app_config.json'
            config_path.parent.mkdir(parents=True, exist_ok=True)

            with open(config_path, 'w') as f:
                json.dump(current_config, f, indent=4)

            st.success("Settings saved successfully!")
        except Exception as e:
            st.error(f"Error saving settings: {str(e)}")