import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta
from pathlib import Path

from app.utils.database import get_study_logs
from app.components.forms import study_log_form
from app.components.charts import plot_study_progress, plot_weekly_study_progress
from app.components.metrics import calculate_streak


# Load configuration
def get_config():
    config_path = Path(__file__).parents[2] / 'config' / 'app_config.json'
    if config_path.exists():
        with open(config_path, 'r') as f:
            return json.load(f)
    else:
        # Default configuration
        return {
            "study_tracking": {
                "daily_target_minutes": 70,
                "weekly_target_days": 5
            }
        }


config = get_config()
daily_target = config.get('study_tracking', {}).get('daily_target_minutes', 70)


def show():
    """Display the study tracker page."""
    # Custom styling for consistent headers
    st.markdown(
        "<h2 style='color: #67597A; border-bottom: 2px solid #E5F77D; padding-bottom: 5px;'>SOA Study Tracker</h2>",
        unsafe_allow_html=True)

    # Create tabs for logging study time and viewing progress
    tab1, tab2, tab3 = st.tabs(["Log Study Time", "Daily Progress", "Weekly Progress"])

    # Get study data from database
    study_df = get_study_logs()

    # Convert date column to datetime if it's not already
    if not study_df.empty:
        study_df['date'] = pd.to_datetime(study_df['date'])

    with tab1:
        # Show the study log form
        log_added = study_log_form()
        if log_added:
            # Display success message (don't use rerun here)
            st.success("Study time logged successfully!")

    with tab2:
        st.markdown("<h3 style='color: #67597A;'>Daily Study Progress</h3>", unsafe_allow_html=True)

        if not study_df.empty:
            # Calculate and display streak
            streak = calculate_streak(study_df)

            # Display metrics in columns
            col1, col2, col3 = st.columns(3)

            with col1:
                total_study_time = study_df['duration'].sum()
                hours = total_study_time // 60
                minutes = total_study_time % 60
                st.metric("Total Study Time", f"{hours}h {minutes}m")

            with col2:
                daily_average = study_df.groupby(study_df['date'].dt.date)['duration'].sum().mean()
                avg_hours = int(daily_average // 60)
                avg_minutes = int(daily_average % 60)
                st.metric("Daily Average", f"{avg_hours}h {avg_minutes}m")

            with col3:
                st.metric("Current Streak", f"{streak} days")

            # Display progress against daily target
            fig = plot_study_progress(study_df, daily_target)

            # Chart container with transparent background and lime border
            st.markdown(
                """
                <style>
                .chart-container {
                    border: 2px solid #E5F77D;
                    padding: 10px;
                    margin-bottom: 20px;
                    background-color: rgba(0, 0, 0, 0.05);
                }
                </style>
                <div class="chart-container">
                """,
                unsafe_allow_html=True
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Study log table
            st.markdown("<h4 style='color: #67597A;'>Study Log</h4>", unsafe_allow_html=True)

            log_view = study_df.sort_values('date', ascending=False).copy()
            log_view['date'] = log_view['date'].dt.date
            log_view['hours'] = log_view['duration'] // 60
            log_view['minutes'] = log_view['duration'] % 60
            log_view['time'] = log_view.apply(lambda x: f"{x['hours']}h {x['minutes']}m", axis=1)

            # Create a more readable dataframe for display
            display_df = log_view[['date', 'time', 'notes']].rename(
                columns={'date': 'Date', 'time': 'Study Time', 'notes': 'Notes'}
            )

            st.dataframe(display_df, use_container_width=True)
        else:
            st.info("No study data recorded yet. Use the 'Log Study Time' tab to get started!")

    with tab3:
        st.markdown("<h3 style='color: #67597A;'>Weekly Study Progress</h3>", unsafe_allow_html=True)

        if not study_df.empty:
            # Weekly progress chart
            fig = plot_weekly_study_progress(study_df, daily_target)

            # Chart container with transparent background and lime border
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Weekly summary statistics
            st.markdown("<h4 style='color: #67597A;'>Weekly Summary</h4>", unsafe_allow_html=True)

            # Create a weekly summary dataframe
            weekly_df = study_df.copy()
            weekly_df['week'] = weekly_df['date'].dt.isocalendar().week
            weekly_df['year'] = weekly_df['date'].dt.isocalendar().year
            weekly_df['year_week'] = weekly_df['year'].astype(str) + '-W' + weekly_df['week'].astype(str)

            weekly_summary = weekly_df.groupby('year_week')['duration'].agg(['sum', 'count']).reset_index()
            weekly_summary.columns = ['Week', 'Total Minutes', 'Study Days']

            # Calculate target and percentage
            weekly_target_minutes = daily_target * 7
            weekly_summary['Target'] = weekly_target_minutes
            weekly_summary['Percentage'] = (weekly_summary['Total Minutes'] / weekly_target_minutes * 100).round(1)

            # Format for display
            weekly_summary['Hours'] = (weekly_summary['Total Minutes'] // 60).astype(int)
            weekly_summary['Minutes'] = (weekly_summary['Total Minutes'] % 60).astype(int)
            weekly_summary['Time'] = weekly_summary.apply(lambda x: f"{x['Hours']}h {x['Minutes']}m", axis=1)

            # Final display dataframe
            display_weekly = weekly_summary[['Week', 'Time', 'Study Days', 'Percentage']].rename(
                columns={'Time': 'Total Time', 'Percentage': 'Target %'}
            )

            # Sort by week (most recent first)
            display_weekly = display_weekly.sort_values('Week', ascending=False)

            st.dataframe(display_weekly, use_container_width=True)

            # Display study consistency information
            st.markdown("<h4 style='color: #67597A;'>Study Consistency</h4>", unsafe_allow_html=True)

            # Get data for the last 4 weeks
            today = datetime.now().date()
            four_weeks_ago = today - timedelta(days=28)
            recent_study = study_df[study_df['date'].dt.date >= four_weeks_ago]

            if not recent_study.empty:
                # Calculate consistency metrics
                study_days = recent_study['date'].dt.date.nunique()
                total_days = (today - four_weeks_ago).days + 1
                consistency_percentage = (study_days / total_days) * 100

                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Study Days (Last 4 Weeks)", f"{study_days}/{total_days}")

                with col2:
                    st.metric("Consistency", f"{consistency_percentage:.1f}%")

                # Show a message based on consistency
                if consistency_percentage >= 80:
                    st.success("Excellent consistency! You're studying regularly, which is key to success.")
                elif consistency_percentage >= 50:
                    st.info("Good consistency. Try to increase your study frequency for better results.")
                else:
                    st.warning(
                        "Your study consistency could be improved. Regular study sessions, even short ones, can make a big difference.")
            else:
                st.info("Not enough recent data to calculate study consistency.")
        else:
            st.info("No study data recorded yet. Use the 'Log Study Time' tab to get started!")