import streamlit as st
import pandas as pd
import json
import os
from pathlib import Path
from io import BytesIO

from app.utils.database import get_all_jobs, get_study_logs, reset_job_data, reset_study_data, reset_all_data
from app.utils.file_handler import export_dataframe


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
    st.title("Settings")

    # App information
    st.sidebar.markdown("---")
    app_name = config.get('app', {}).get('name', "Job Hunt & Study Tracker")
    app_version = config.get('app', {}).get('version', "1.0.0")
    st.sidebar.info(f"{app_name} v{app_version}")

    # Create tabs for different settings sections
    tab1, tab2, tab3 = st.tabs(["Export Data", "Reset Data", "Application Settings"])

    with tab1:
        show_export_options()

    with tab2:
        show_reset_options()

    with tab3:
        show_app_settings()


def show_export_options():
    """Display options for exporting data."""
    st.header("Export Data")

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
    st.header("Reset Data")
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
    st.subheader("Reset All Data")

    # Create a confirmation check
    confirm_reset = st.checkbox("I understand this will delete ALL my data and cannot be undone.")

    if confirm_reset:
        if st.button("Reset ALL Data"):
            with st.spinner("Resetting all data..."):
                reset_all_data()
                st.success("All data has been reset!")


def show_app_settings():
    """Display application settings."""
    st.header("Application Settings")

    # Load current configuration
    current_config = get_config()

    # Study settings
    st.subheader("Study Settings")

    daily_target = st.number_input(
        "Daily Study Target (minutes)",
        min_value=5,
        max_value=480,
        value=current_config.get('study_tracking', {}).get('daily_target_minutes', 70),
        step=5
    )

    weekly_target_days = st.number_input(
        "Weekly Target Days",
        min_value=1,
        max_value=7,
        value=current_config.get('study_tracking', {}).get('weekly_target_days', 5),
        step=1
    )

    # Job application settings
    st.subheader("Job Application Settings")

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
                'daily_target_minutes': daily_target,
                'weekly_target_days': weekly_target_days
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
            st.rerun()  # Changed from experimental_rerun() to rerun()
        except Exception as e:
            st.error(f"Error saving settings: {str(e)}")