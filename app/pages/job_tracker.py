import streamlit as st
import pandas as pd
import json
from datetime import datetime
import os
from pathlib import Path

from app.utils.database import get_all_jobs, update_job, get_job, delete_job
from app.utils.file_handler import get_file_download_link, save_resume, save_cover_letter, delete_file
from app.components.forms import job_application_form


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
            }
        }


config = get_config()
status_options = config.get('job_tracking', {}).get('statuses', [
    "Applied", "No Response", "Rejected", "Screening Call",
    "Interview", "Second Interview", "Final Interview",
    "Offer", "Accepted", "Declined"
])


def show():
    """Display the job applications tracker page."""
    st.title("Job Applications Tracker")

    # Create tabs for adding new applications and viewing/updating existing ones
    tab1, tab2 = st.tabs(["Add New Application", "View/Update Applications"])

    with tab1:
        # Show the job application form
        job_added = job_application_form()
        if job_added:
            # Display success message (don't use rerun here)
            st.success("Job application added successfully!")

    with tab2:
        st.header("View and Update Job Applications")

        # Get job data from database
        jobs_df = get_all_jobs()

        if not jobs_df.empty:
            # Add filter options
            col1, col2 = st.columns(2)

            with col1:
                status_filter = st.multiselect(
                    "Filter by Status",
                    options=status_options,
                    default=[]
                )

            with col2:
                search_term = st.text_input("Search by Company or Position", "")

            # Apply filters
            filtered_df = jobs_df.copy()

            if status_filter:
                filtered_df = filtered_df[filtered_df['status'].isin(status_filter)]

            if search_term:
                search_mask = (
                        filtered_df['company'].str.contains(search_term, case=False) |
                        filtered_df['position'].str.contains(search_term, case=False)
                )
                filtered_df = filtered_df[search_mask]

            # Display a list of applications with expandable details
            for index, job in filtered_df.iterrows():
                with st.expander(f"{job['company']} - {job['position']} ({job['status']})"):
                    update_job_details(job)
        else:
            st.info("No job applications added yet. Use the 'Add New Application' tab to get started!")


def update_job_details(job):
    """
    Display and allow updating of a job application's details.

    Args:
        job: Series containing job application data
    """
    job_id = job['id']
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Company:** {job['company']}")
        st.write(f"**Position:** {job['position']}")
        st.write(f"**Date Applied:** {job['date_applied']}")
        st.write(f"**Last Updated:** {job['last_updated']}")

        # Allow updating status
        new_status = st.selectbox(
            "Update Status",
            status_options,
            index=status_options.index(job['status']) if job['status'] in status_options else 0,
            key=f"status_{job_id}"
        )

        # Update notes
        new_notes = st.text_area("Update Notes", value=job['notes'], key=f"notes_{job_id}")

    with col2:
        # Display resume and cover letter download links
        st.write("**Resume:**")
        if job['resume_path']:
            resume_file_name = os.path.basename(job['resume_path'])
            st.markdown(get_file_download_link(job['resume_path'], resume_file_name), unsafe_allow_html=True)
        else:
            st.write("No resume uploaded")

        # Upload new resume
        new_resume = st.file_uploader("Upload New Resume", type=["pdf", "docx", "doc"], key=f"new_resume_{job_id}")

        st.write("**Cover Letter:**")
        if job['cover_letter_path']:
            cover_letter_file_name = os.path.basename(job['cover_letter_path'])
            st.markdown(get_file_download_link(job['cover_letter_path'], cover_letter_file_name),
                        unsafe_allow_html=True)
        else:
            st.write("No cover letter uploaded")

        # Upload new cover letter
        new_cover_letter = st.file_uploader("Upload New Cover Letter", type=["pdf", "docx", "doc"],
                                            key=f"new_cover_{job_id}")

    # Status history timeline
    if job['notes'] and "STATUS HISTORY" in job['notes']:
        st.write("**Status History:**")
        st.info(job['notes'].split("STATUS HISTORY")[1])

    # Add columns for the buttons
    col1, col2 = st.columns(2)

    # Save button for updates
    with col1:
        if st.button("Save Changes", key=f"save_{job_id}"):
            # Process file uploads if any
            resume_path = job['resume_path']
            cover_letter_path = job['cover_letter_path']

            if new_resume:
                resume_path = save_resume(new_resume, job['company'], job['position'])

            if new_cover_letter:
                cover_letter_path = save_cover_letter(new_cover_letter, job['company'], job['position'])

            # Add status history to notes if status has changed
            if new_status != job['status']:
                status_history = job['notes']
                if "STATUS HISTORY" not in status_history:
                    status_history += "\n\nSTATUS HISTORY\n"

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                status_history += f"\n{timestamp}: Changed from '{job['status']}' to '{new_status}'"
                new_notes = status_history

            # Update database
            update_job(
                job_id=job_id,
                status=new_status,
                notes=new_notes,
                resume_path=resume_path,
                cover_letter_path=cover_letter_path
            )

            st.success("Job application updated!")
            # Don't use rerun here

    # Delete button with confirmation
    with col2:
        if st.button("Delete Application", key=f"delete_{job_id}", type="secondary"):
            st.session_state[f"confirm_delete_{job_id}"] = True

    # Show confirmation dialog if delete button was clicked
    if st.session_state.get(f"confirm_delete_{job_id}", False):
        st.warning("Are you sure you want to delete this job application? This action cannot be undone.")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Yes, Delete", key=f"confirm_yes_{job_id}", type="primary"):
                # Delete associated files if they exist
                if job['resume_path']:
                    delete_file(job['resume_path'])

                if job['cover_letter_path']:
                    delete_file(job['cover_letter_path'])

                # Delete the job from the database
                delete_job(job_id)

                st.success("Job application deleted successfully!")
                st.session_state[f"confirm_delete_{job_id}"] = False
                # Don't use rerun here - just update the session state
                # The user can manually refresh the page if needed

        with col2:
            if st.button("Cancel", key=f"confirm_no_{job_id}", type="secondary"):
                st.session_state[f"confirm_delete_{job_id}"] = False
                # Don't use rerun here