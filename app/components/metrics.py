import random
import streamlit as st
from datetime import datetime, timedelta
import pandas as pd


def display_metrics(jobs_df, study_df):
    """
    Calculate and display key metrics for the dashboard.

    Args:
        jobs_df: DataFrame containing job application data
        study_df: DataFrame containing study log data

    Returns:
        tuple: (application_progress, study_progress) - Progress metrics
    """
    # Calculate job metrics
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

    return application_progress, study_progress


def display_affirmation(job_progress, study_progress):
    """
    Generate a motivational affirmation based on progress.

    Args:
        job_progress: Float between 0 and 1 representing job application progress
        study_progress: Float between 0 and 1 representing study progress

    Returns:
        str: A motivational affirmation
    """
    affirmations = [
        "You're making excellent progress! Keep up the great work!",
        "Every application brings you closer to your goal. Stay persistent!",
        "Your dedication to studying will pay off. Keep going!",
        "You're developing great habits for success. Well done!",
        "Focus on progress, not perfection. You're doing great!",
        "Your consistent efforts will lead to great results!",
        "Small steps every day lead to big achievements!",
        "You're taking control of your career journey. Impressive!",
        "Your determination is inspiring. Keep pushing forward!"
    ]

    # Add more specific affirmations based on progress
    job_specific = [
        "Your job search strategy is working! Keep refining your approach.",
        "Each application is a learning opportunity. You're growing with each one!",
        "The right opportunity is coming your way. Stay persistent!",
        "Your hard work in the job search will pay off soon."
    ]

    study_specific = [
        "Your consistent study habits are building a strong foundation for success.",
        "Every minute of study is an investment in your future.",
        "Your dedication to learning will set you apart in your career.",
        "Small, consistent study sessions add up to significant progress over time."
    ]

    # Select the appropriate affirmation based on progress
    if job_progress > 0.8 and study_progress > 0.8:
        return random.choice(affirmations) + " You're excelling in both job hunting and studying!"
    elif job_progress > 0.8:
        return random.choice(job_specific) + " Your job search is going strong!"
    elif study_progress > 0.8:
        return random.choice(study_specific) + " Your study habits are excellent!"
    elif job_progress > 0.5 and study_progress > 0.5:
        return random.choice(affirmations) + " You're making solid progress on all fronts."
    elif job_progress < 0.3 and study_progress < 0.3:
        return "Remember, progress takes time. Stay consistent and keep pushing forward!"
    else:
        return random.choice(affirmations)


def calculate_streak(study_df):
    """
    Calculate the current study streak.

    Args:
        study_df: DataFrame containing study log data

    Returns:
        int: The current streak in days
    """
    if study_df.empty:
        return 0

    # Convert date column to datetime if it's not already
    study_df['date'] = pd.to_datetime(study_df['date'])

    # Get all unique dates with study sessions
    dates = sorted(study_df['date'].dt.date.unique())

    if not dates:
        return 0

    current_date = datetime.now().date()
    yesterday = current_date - timedelta(days=1)

    # If the most recent study date is more than a day old, streak is broken
    if dates[-1] < yesterday:
        return 0

    # Count consecutive days backward from the most recent date
    streak = 1  # Start with 1 for the most recent day
    for i in range(len(dates) - 1, 0, -1):
        if (dates[i] - dates[i - 1]).days == 1:
            streak += 1
        else:
            break

    return streak


def get_progress_color(progress):
    """
    Return an appropriate color based on progress level.

    Args:
        progress: Float between 0 and 1 representing progress

    Returns:
        str: A color code
    """
    if progress >= 0.8:
        return "#E5F77D"  # Bright lime - success
    elif progress >= 0.5:
        return "#E9724C"  # Coral - warning/caution
    else:
        return "#67597A"  # Deep purple - needs improvement