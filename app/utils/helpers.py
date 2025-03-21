"""
Helper functions for the Job Hunt & Study Tracker application.
"""

import calendar
import datetime
import pandas as pd
import numpy as np
import json
from pathlib import Path


def get_config():
    """
    Load application configuration from the config file.

    Returns:
        dict: Application configuration
    """
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
            },
            "database": {
                "path": "data/database/job_hunt_tracker.db"
            },
            "uploads": {
                "path": "data/uploads",
                "allowed_extensions": ["pdf", "docx", "doc", "txt"]
            },
            "job_tracking": {
                "weekly_goal": 5,
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
                "daily_target_minutes": 70,
                "weekly_target_days": 5
            },
            "ui": {
                "theme_color": "#4C78A8",
                "secondary_color": "#59A14F",
                "warning_color": "#E15759",
                "affirmations_enabled": True
            }
        }


def get_date_range(start_date, end_date):
    """
    Generate a list of dates between start_date and end_date (inclusive).

    Args:
        start_date: Starting date
        end_date: Ending date

    Returns:
        list: List of datetime.date objects
    """
    delta = end_date - start_date
    return [start_date + datetime.timedelta(days=i) for i in range(delta.days + 1)]


def get_week_dates(year, week):
    """
    Get the start and end dates for a given year and week number.

    Args:
        year: Year (e.g. 2023)
        week: ISO week number (1-53)

    Returns:
        tuple: (start_date, end_date) for the week
    """
    first_day_of_year = datetime.date(year, 1, 1)
    first_week_day = first_day_of_year.weekday()
    days_to_first_monday = (7 - first_week_day) % 7

    first_monday = first_day_of_year + datetime.timedelta(days=days_to_first_monday)
    start_date = first_monday + datetime.timedelta(weeks=week - 1)
    end_date = start_date + datetime.timedelta(days=6)

    return start_date, end_date


def calculate_application_stats(jobs_df):
    """
    Calculate statistics from job application data.

    Args:
        jobs_df: DataFrame containing job application data

    Returns:
        dict: Dictionary of calculated statistics
    """
    if jobs_df.empty:
        return {
            'total_applications': 0,
            'application_rate_per_week': 0,
            'interview_rate': 0,
            'avg_response_time': 0,
            'active_applications': 0
        }

    # Convert date columns to datetime
    jobs_df['date_applied'] = pd.to_datetime(jobs_df['date_applied'])
    jobs_df['last_updated'] = pd.to_datetime(jobs_df['last_updated'])

    # Total applications
    total_applications = len(jobs_df)

    # Calculate application rate per week
    if len(jobs_df) >= 2:
        date_range = (jobs_df['date_applied'].max() - jobs_df['date_applied'].min()).days
        weeks = max(1, date_range / 7)
        application_rate_per_week = total_applications / weeks
    else:
        application_rate_per_week = total_applications

    # Interview rate
    interview_statuses = ['Interview', 'Second Interview', 'Final Interview', 'Offer', 'Accepted']
    interviews = jobs_df[jobs_df['status'].isin(interview_statuses)]
    interview_rate = len(interviews) / total_applications if total_applications > 0 else 0

    # Calculate average response time (days between application and first status change)
    response_times = []
    for _, job in jobs_df.iterrows():
        if job['status'] != 'Applied' and job['status'] != 'No Response':
            # Assuming status changes are recorded in the last_updated field
            response_time = (job['last_updated'] - job['date_applied']).days
            response_times.append(response_time)

    avg_response_time = np.mean(response_times) if response_times else 0

    # Count active applications (not rejected, accepted, or declined)
    inactive_statuses = ['Rejected', 'Accepted', 'Declined']
    active_applications = len(jobs_df[~jobs_df['status'].isin(inactive_statuses)])

    return {
        'total_applications': total_applications,
        'application_rate_per_week': round(application_rate_per_week, 1),
        'interview_rate': round(interview_rate * 100, 1),
        'avg_response_time': round(avg_response_time, 1),
        'active_applications': active_applications
    }


def calculate_study_stats(study_df):
    """
    Calculate statistics from study log data.

    Args:
        study_df: DataFrame containing study log data

    Returns:
        dict: Dictionary of calculated statistics
    """
    if study_df.empty:
        return {
            'total_study_time': 0,
            'avg_daily_time': 0,
            'study_days': 0,
            'current_streak': 0,
            'longest_streak': 0,
            'weekly_consistency': 0
        }

    # Convert date column to datetime
    study_df['date'] = pd.to_datetime(study_df['date'])

    # Total study time in minutes
    total_study_time = study_df['duration'].sum()

    # Average daily study time
    study_days = study_df['date'].dt.date.nunique()
    avg_daily_time = total_study_time / study_days if study_days > 0 else 0

    # Calculate current streak
    dates = sorted(study_df['date'].dt.date.unique())
    current_date = datetime.datetime.now().date()
    yesterday = current_date - datetime.timedelta(days=1)

    current_streak = 0
    if dates and dates[-1] >= yesterday:
        current_streak = 1
        for i in range(len(dates) - 1, 0, -1):
            if (dates[i] - dates[i - 1]).days == 1:
                current_streak += 1
            else:
                break

    # Calculate longest streak
    longest_streak = 1
    current = 1
    for i in range(1, len(dates)):
        if (dates[i] - dates[i - 1]).days == 1:
            current += 1
        else:
            longest_streak = max(longest_streak, current)
            current = 1

    longest_streak = max(longest_streak, current)

    # Calculate weekly consistency (percentage of days studied in the last 28 days)
    four_weeks_ago = current_date - datetime.timedelta(days=28)
    days_in_range = (current_date - four_weeks_ago).days + 1

    recent_dates = [d for d in dates if d >= four_weeks_ago]
    weekly_consistency = len(recent_dates) / days_in_range if days_in_range > 0 else 0

    return {
        'total_study_time': total_study_time,
        'avg_daily_time': round(avg_daily_time, 1),
        'study_days': study_days,
        'current_streak': current_streak,
        'longest_streak': longest_streak,
        'weekly_consistency': round(weekly_consistency * 100, 1)
    }


def format_time_from_minutes(minutes):
    """
    Format minutes as hours and minutes string.

    Args:
        minutes: Total minutes

    Returns:
        str: Formatted time string (e.g. "2h 15m")
    """
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}h {mins}m"


def parse_time_to_minutes(time_str):
    """
    Parse a time string into minutes.

    Args:
        time_str: Time string (e.g. "2h 15m", "2:15", "2.25")

    Returns:
        int: Total minutes
    """
    if not time_str:
        return 0

    # Handle format like "2h 15m"
    if 'h' in time_str.lower() and 'm' in time_str.lower():
        parts = time_str.lower().replace('h', ' ').replace('m', ' ').split()
        hours = int(parts[0])
        minutes = int(parts[1])
        return hours * 60 + minutes

    # Handle format like "2:15"
    if ':' in time_str:
        hours, minutes = time_str.split(':')
        return int(hours) * 60 + int(minutes)

    # Handle format like "2.25" (decimal hours)
    try:
        hours = float(time_str)
        return int(hours * 60)
    except ValueError:
        return 0