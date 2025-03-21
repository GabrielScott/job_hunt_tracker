import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

from app.utils.database import get_all_jobs, get_study_logs
from app.components.metrics import display_metrics, display_affirmation
from app.components.charts import plot_applications_over_time, plot_status_distribution, plot_study_progress


def show():
    """Display the main dashboard page."""
    st.title("Job Hunt & Study Progress Dashboard")

    # Get job application and study data
    jobs_df = get_all_jobs()
    study_df = get_study_logs()

    # Convert date columns to datetime
    if not jobs_df.empty:
        jobs_df['date_applied'] = pd.to_datetime(jobs_df['date_applied'])
        jobs_df['last_updated'] = pd.to_datetime(jobs_df['last_updated'])

    if not study_df.empty:
        study_df['date'] = pd.to_datetime(study_df['date'])

    # Calculate metrics
    total_applications = len(jobs_df) if not jobs_df.empty else 0
    interview_count = len(jobs_df[jobs_df['status'].isin(
        ['Interview', 'Second Interview', 'Final Interview'])]) if not jobs_df.empty else 0

    # Calculate study progress for the last 7 days
    today = datetime.now().date()
    last_week = today - timedelta(days=7)

    recent_study = study_df[
        pd.to_datetime(study_df['date']).dt.date >= last_week] if not study_df.empty else pd.DataFrame()
    total_minutes = recent_study['duration'].sum() if not recent_study.empty else 0

    daily_target = 70  # 1h10m in minutes
    weekly_target = daily_target * 7
    study_progress = min(total_minutes / weekly_target, 1) if weekly_target > 0 else 0

    # Weekly application goal (assuming 5 applications per week)
    weekly_goal = 5
    recent_applications = len(
        jobs_df[pd.to_datetime(jobs_df['date_applied']).dt.date >= last_week]) if not jobs_df.empty else 0
    application_progress = min(recent_applications / weekly_goal, 1) if weekly_goal > 0 else 0

    # Display metrics in columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Applications", total_applications)

    with col2:
        st.metric("Interview Rate", f"{interview_count}/{total_applications}" if total_applications > 0 else "0/0")

    with col3:
        st.metric("Weekly Study Progress", f"{int(study_progress * 100)}%")

    with col4:
        st.metric("Weekly Application Goal", f"{recent_applications}/{weekly_goal}")

    # Display affirmation
    st.markdown("### Daily Affirmation")
    st.info(display_affirmation(application_progress, study_progress))

    # Applications over time chart
    st.markdown("### Application Trends")
    if not jobs_df.empty:
        fig = plot_applications_over_time(jobs_df)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No application data available yet. Start adding job applications to see trends.")

    # Status distribution chart
    st.markdown("### Application Status Distribution")
    if not jobs_df.empty and len(jobs_df['status'].unique()) > 1:
        fig = plot_status_distribution(jobs_df)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Not enough application data with different statuses available yet.")

    # Study progress chart
    st.markdown("### Study Progress")
    if not study_df.empty:
        fig = plot_study_progress(study_df, daily_target)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No study data available yet. Start logging your study time to see progress.")

    # Recent activities
    st.markdown("### Recent Activities")

    tab1, tab2 = st.tabs(["Recent Applications", "Recent Study Sessions"])

    with tab1:
        if not jobs_df.empty:
            # Make sure we have unique job entries by company and position
            # Since job_id is not visible to users, we'll use company+position as a proxy for uniqueness
            # This will help eliminate any visual duplicates
            jobs_df['company_position'] = jobs_df['company'] + ' - ' + jobs_df['position']
            recent_jobs = jobs_df.drop_duplicates(subset=['company_position']).sort_values('date_applied',
                                                                                           ascending=False).head(5)

            for _, job in recent_jobs.iterrows():
                st.markdown(f"**{job['company']} - {job['position']}** ({job['status']})")
                st.markdown(f"Applied on: {job['date_applied'].strftime('%Y-%m-%d')}")
                if job['notes']:
                    # Truncate notes if they are too long for the dashboard view
                    display_notes = job['notes']
                    if len(display_notes) > 100:  # Limit to 100 characters
                        display_notes = display_notes[:97] + "..."
                    st.markdown(f"Notes: {display_notes}")
                st.markdown("---")
        else:
            st.write("No recent job applications.")

    with tab2:
        if not study_df.empty:
            recent_study = study_df.sort_values('date', ascending=False).head(5)
            for _, session in recent_study.iterrows():
                hours = session['duration'] // 60
                minutes = session['duration'] % 60
                st.markdown(f"**{session['date'].strftime('%Y-%m-%d')}** - Studied for {hours}h {minutes}m")
                if session['notes']:
                    st.markdown(f"Notes: {session['notes']}")
                st.markdown("---")
        else:
            st.write("No recent study sessions.")