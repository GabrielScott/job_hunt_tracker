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
    # Title is now handled by the header in main.py
    # We use a smaller subtitle here if needed
    st.markdown("### Your Dashboard Overview", unsafe_allow_html=True)

    # Get job application and study data
    jobs_df = get_all_jobs()
    study_df = get_study_logs()

    # Convert date columns to datetime
    if not jobs_df.empty:
        jobs_df['date_applied'] = pd.to_datetime(jobs_df['date_applied'])
        jobs_df['last_updated'] = pd.to_datetime(jobs_df['last_updated'])

    if not study_df.empty:
        study_df['date'] = pd.to_datetime(study_df['date'])

    # Use the metrics component to display key metrics
    application_progress, study_progress = display_metrics(jobs_df, study_df)

    # Display affirmation in a clean styled box
    st.markdown(
        f"""
        <div style="
            background-color: #F4F7BE;
            border-left: 4px solid #E5F77D;
            padding: 15px;
            margin: 10px 0;
            font-family: 'Courier New', monospace;
            color: #67597A;
            font-weight: bold;
        ">
            ✨ {display_affirmation(application_progress, study_progress)}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Applications over time chart - lime green header
    st.markdown(
        "<h3 style='color: #E5F77D; border-bottom: 2px solid #E5F77D; padding-bottom: 5px;'>Application Trends</h3>",
        unsafe_allow_html=True)

    if not jobs_df.empty:
        # Create the chart directly without the container div
        fig = plot_applications_over_time(jobs_df)
        # Update chart layout for dark/transparent background
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0.05)',
            font=dict(color="#E5F77D")
        )
        # Draw a border around the chart using CSS
        st.markdown("""
        <style>
        [data-testid="stPlotlyChart"] {
            border: 2px solid #E5F77D;
            padding: 10px;
            margin-bottom: 20px;
            background-color: rgba(0, 0, 0, 0.05);
        }
        </style>
        """, unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown(
            """
            <div style="
                background-color: #F4F7BE;
                border: 2px solid #E5F77D;
                padding: 15px;
                text-align: center;
                color: #67597A;
                font-family: 'Courier New', monospace;
            ">
                📋 No application data available yet. Start adding job applications to see trends.
            </div>
            """,
            unsafe_allow_html=True
        )

    # Status distribution chart - lime green header
    st.markdown(
        "<h3 style='color: #E5F77D; border-bottom: 2px solid #E5F77D; padding-bottom: 5px;'>Application Status Distribution</h3>",
        unsafe_allow_html=True)

    if not jobs_df.empty and len(jobs_df['status'].unique()) > 1:
        # Create the chart directly without the container div
        fig = plot_status_distribution(jobs_df)
        # Update chart layout for dark/transparent background
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0.05)',
            font=dict(color="#E5F77D")
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown(
            """
            <div style="
                background-color: #F4F7BE;
                border: 2px solid #E5F77D;
                padding: 15px;
                text-align: center;
                color: #67597A;
                font-family: 'Courier New', monospace;
            ">
                📊 Not enough application data with different statuses available yet.
            </div>
            """,
            unsafe_allow_html=True
        )

    # Study progress chart - lime green header
    st.markdown(
        "<h3 style='color: #E5F77D; border-bottom: 2px solid #E5F77D; padding-bottom: 5px;'>Study Progress</h3>",
        unsafe_allow_html=True)

    if not study_df.empty:
        # Create the chart directly without the container div
        fig = plot_study_progress(study_df)
        # Update chart layout for dark/transparent background
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0.05)',
            font=dict(color="#E5F77D")
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown(
            """
            <div style="
                background-color: #F4F7BE;
                border: 2px solid #E5F77D;
                padding: 15px;
                text-align: center;
                color: #67597A;
                font-family: 'Courier New', monospace;
            ">
                📚 No study data available yet. Start logging your study time to see progress.
            </div>
            """,
            unsafe_allow_html=True
        )

    # Recent activities section - lime green header
    st.markdown(
        "<h3 style='color: #E5F77D; border-bottom: 2px solid #E5F77D; padding-bottom: 5px;'>Recent Activities</h3>",
        unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # Recent Applications Header
        st.markdown(
            """
            <div style="
                background-color: #67597A;
                padding: 10px;
                text-align: center;
                color: #F4F7BE;
                font-family: 'Courier New', monospace;
                font-weight: bold;
                border: 2px solid #E5F77D;
                border-bottom: none;
            ">
                Recent Applications
            </div>
            """,
            unsafe_allow_html=True
        )

        # Recent Applications Content
        if not jobs_df.empty:
            # Make sure we have unique job entries by company and position
            jobs_df['company_position'] = jobs_df['company'] + ' - ' + jobs_df['position']
            recent_jobs = jobs_df.drop_duplicates(subset=['company_position']).sort_values('date_applied',
                                                                                           ascending=False).head(5)

            # Create a container div for the content
            recent_container = '<div style="border: 2px solid #E5F77D; border-top: none; padding: 10px; height: 300px; overflow-y: auto;">'

            for _, job in recent_jobs.iterrows():
                job_date = job['date_applied'].strftime('%Y-%m-%d')

                # Format notes with ellipsis if too long
                notes = job['notes'] if job['notes'] else ""
                if len(notes) > 100:
                    notes = notes[:97] + "..."

                recent_container += f"""
                <div style="margin-bottom: 15px; padding-bottom: 15px; border-bottom: 1px solid #E5F77D;">
                    <div style="font-weight: bold; color: #67597A;">{job['company']} - {job['position']} ({job['status']})</div>
                    <div style="color: #757761;">Applied on: {job_date}</div>
                """

                if notes:
                    recent_container += f'<div style="color: #757761; font-style: italic; margin-top: 5px;">Notes: {notes}</div>'

                recent_container += '</div>'

            recent_container += '</div>'
            st.markdown(recent_container, unsafe_allow_html=True)
        else:
            # Empty state for no applications
            st.markdown(
                """
                <div style="
                    border: 2px solid #E5F77D;
                    border-top: none;
                    padding: 20px;
                    text-align: center;
                    color: #757761;
                    height: 300px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-family: 'Courier New', monospace;
                ">
                    No recent job applications.
                </div>
                """,
                unsafe_allow_html=True
            )

    with col2:
        # Recent Study Sessions Header
        st.markdown(
            """
            <div style="
                background-color: #67597A;
                padding: 10px;
                text-align: center;
                color: #F4F7BE;
                font-family: 'Courier New', monospace;
                font-weight: bold;
                border: 2px solid #E5F77D;
                border-bottom: none;
            ">
                Recent Study Sessions
            </div>
            """,
            unsafe_allow_html=True
        )

        # Recent Study Sessions Content
        if not study_df.empty:
            recent_study = study_df.sort_values('date', ascending=False).head(5)

            # Create a container div for the content
            study_container = '<div style="border: 2px solid #E5F77D; border-top: none; padding: 10px; height: 300px; overflow-y: auto;">'

            for _, session in recent_study.iterrows():
                session_date = session['date'].strftime('%Y-%m-%d')
                hours = session['duration'] // 60
                minutes = session['duration'] % 60

                # Format notes
                notes = session['notes'] if session['notes'] else ""

                study_container += f"""
                <div style="margin-bottom: 15px; padding-bottom: 15px; border-bottom: 1px solid #E5F77D;">
                    <div style="font-weight: bold; color: #67597A;">{session_date}</div>
                    <div style="color: #757761;">Studied for {hours}h {minutes}m</div>
                """

                if notes:
                    study_container += f'<div style="color: #757761; font-style: italic; margin-top: 5px;">Notes: {notes}</div>'

                study_container += '</div>'

            study_container += '</div>'
            st.markdown(study_container, unsafe_allow_html=True)
        else:
            # Empty state for no study sessions
            st.markdown(
                """
                <div style="
                    border: 2px solid #E5F77D;
                    border-top: none;
                    padding: 20px;
                    text-align: center;
                    color: #757761;
                    height: 300px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-family: 'Courier New', monospace;
                ">
                    No recent study sessions.
                </div>
                """,
                unsafe_allow_html=True
            )