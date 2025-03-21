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

    # Applications over time chart
    st.markdown("### Application Trends")
    if not jobs_df.empty:
        fig = plot_applications_over_time(jobs_df)
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

    # Status distribution chart
    st.markdown("### Application Status Distribution")
    if not jobs_df.empty and len(jobs_df['status'].unique()) > 1:
        fig = plot_status_distribution(jobs_df)
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

    # Study progress chart
    st.markdown("### Study Progress")
    if not study_df.empty:
        fig = plot_study_progress(study_df)
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

    # Recent activities section with custom styling
    st.markdown("### Recent Activities")

    col1, col2 = st.columns(2)

    with col1:
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

        recent_container = """
        <div style="
            border: 2px solid #E5F77D;
            border-top: none;
            padding: 10px;
            font-family: 'Courier New', monospace;
            height: 300px;
            overflow-y: auto;
        ">
        """

        if not jobs_df.empty:
            # Make sure we have unique job entries by company and position
            jobs_df['company_position'] = jobs_df['company'] + ' - ' + jobs_df['position']
            recent_jobs = jobs_df.drop_duplicates(subset=['company_position']).sort_values('date_applied',
                                                                                           ascending=False).head(5)

            for _, job in recent_jobs.iterrows():
                recent_container += f"""
                <div style="margin-bottom: 15px; padding-bottom: 15px; border-bottom: 1px solid #E5F77D;">
                    <div style="font-weight: bold; color: #67597A;">
                        {job['company']} - {job['position']} ({job['status']})
                    </div>
                    <div style="color: #757761;">
                        Applied on: {job['date_applied'].strftime('%Y-%m-%d')}
                    </div>
                """

                if job['notes']:
                    # Truncate notes if they are too long for the dashboard view
                    display_notes = job['notes']
                    if len(display_notes) > 100:  # Limit to 100 characters
                        display_notes = display_notes[:97] + "..."
                    recent_container += f"""
                    <div style="color: #757761; font-style: italic; margin-top: 5px;">
                        Notes: {display_notes}
                    </div>
                    """

                recent_container += "</div>"
        else:
            recent_container += """
            <div style="text-align: center; padding: 20px; color: #757761;">
                No recent job applications.
            </div>
            """

        recent_container += "</div>"
        st.markdown(recent_container, unsafe_allow_html=True)

    with col2:
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

        study_container = """
        <div style="
            border: 2px solid #E5F77D;
            border-top: none;
            padding: 10px;
            font-family: 'Courier New', monospace;
            height: 300px;
            overflow-y: auto;
        ">
        """

        if not study_df.empty:
            recent_study = study_df.sort_values('date', ascending=False).head(5)
            for _, session in recent_study.iterrows():
                hours = session['duration'] // 60
                minutes = session['duration'] % 60
                study_container += f"""
                <div style="margin-bottom: 15px; padding-bottom: 15px; border-bottom: 1px solid #E5F77D;">
                    <div style="font-weight: bold; color: #67597A;">
                        {session['date'].strftime('%Y-%m-%d')}
                    </div>
                    <div style="color: #757761;">
                        Studied for {hours}h {minutes}m
                    </div>
                """

                if session['notes']:
                    study_container += f"""
                    <div style="color: #757761; font-style: italic; margin-top: 5px;">
                        Notes: {session['notes']}
                    </div>
                    """

                study_container += "</div>"
        else:
            study_container += """
            <div style="text-align: center; padding: 20px; color: #757761;">
                No recent study sessions.
            </div>
            """

        study_container += "</div>"
        st.markdown(study_container, unsafe_allow_html=True)