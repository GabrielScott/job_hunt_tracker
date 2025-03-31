import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from app.utils.helpers import calculate_daily_target, get_config


# New color palette
COLOR_PRIMARY = "#67597A"     # Deep purple
COLOR_SECONDARY = "#757761"   # Olive gray
COLOR_ACCENT = "#E9724C"      # Coral orange
COLOR_SUCCESS = "#E5F77D"     # Bright lime
COLOR_BACKGROUND = "#F4F7BE"  # Light cream
COLOR_TEXT = "#E5F77D"        # Lime for text


def plot_applications_over_time(jobs_df):
    """
    Create a chart showing job applications over time.

    Args:
        jobs_df: DataFrame containing job application data

    Returns:
        plotly.graph_objects.Figure: Applications over time chart
    """
    jobs_df['date_applied'] = pd.to_datetime(jobs_df['date_applied'])
    jobs_by_date = jobs_df.groupby(jobs_df['date_applied'].dt.date).size().reset_index(name='count')
    jobs_by_date.columns = ['Date', 'Applications']

    # Calculate cumulative applications
    jobs_by_date['Cumulative'] = jobs_by_date['Applications'].cumsum()

    # Create a date range for all dates in the range
    if len(jobs_by_date) > 1:
        date_range = pd.date_range(start=jobs_by_date['Date'].min(), end=jobs_by_date['Date'].max())
        complete_date_df = pd.DataFrame({'Date': date_range})
        complete_date_df['Date'] = complete_date_df['Date'].dt.date
        jobs_by_date = pd.merge(complete_date_df, jobs_by_date, on='Date', how='left').fillna(0)

        # Recalculate cumulative after filling missing dates
        jobs_by_date['Cumulative'] = jobs_by_date['Applications'].cumsum()

    # Create the chart with new color scheme
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=jobs_by_date['Date'],
        y=jobs_by_date['Applications'],
        name='Daily Applications',
        marker_color=COLOR_PRIMARY
    ))
    fig.add_trace(go.Scatter(
        x=jobs_by_date['Date'],
        y=jobs_by_date['Cumulative'],
        name='Cumulative',
        mode='lines+markers',
        line=dict(color=COLOR_ACCENT, width=3)
    ))

    fig.update_layout(
        title='Application Trends Over Time',
        xaxis_title='Date',
        yaxis_title='Applications',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color=COLOR_TEXT)
        ),
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0.05)',
        font=dict(
            family="Courier New, monospace",
            color=COLOR_TEXT
        ),
        xaxis=dict(
            gridcolor=COLOR_PRIMARY,
            zerolinecolor=COLOR_PRIMARY
        ),
        yaxis=dict(
            gridcolor=COLOR_PRIMARY,
            zerolinecolor=COLOR_PRIMARY
        )
    )

    return fig


def plot_status_distribution(jobs_df):
    """
    Create a pie chart showing distribution of job application statuses.

    Args:
        jobs_df: DataFrame containing job application data

    Returns:
        plotly.graph_objects.Figure: Status distribution pie chart
    """
    status_counts = jobs_df['status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']

    # Define a custom color sequence for different statuses using our palette
    color_map = {
        'Applied': COLOR_PRIMARY,
        'No Response': COLOR_SECONDARY,
        'Rejected': COLOR_ACCENT,
        'Screening Call': COLOR_SUCCESS,
        'Interview': "#8F9973",  # Darker olive
        'Second Interview': "#938BA1",  # Lighter purple
        'Final Interview': "#79695C",  # Brown shade
        'Offer': "#F6D300",  # Gold
        'Accepted': "#AEDB39",  # Lime green
        'Declined': "#FF9770"   # Light coral
    }

    # Get colors for the statuses in our data
    colors = [color_map.get(status, COLOR_ACCENT) for status in status_counts['Status']]

    fig = px.pie(
        status_counts,
        values='Count',
        names='Status',
        title='Application Status Distribution',
        color_discrete_sequence=colors
    )

    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        marker=dict(line=dict(color='rgba(0,0,0,0.2)', width=2))
    )

    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.1,
            xanchor="center",
            x=0.5,
            font=dict(color=COLOR_TEXT)
        ),
        margin=dict(t=60, b=60, l=20, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0.05)',
        font=dict(
            family="Courier New, monospace",
            color=COLOR_TEXT
        )
    )

    return fig


def plot_study_progress(study_df, daily_target=None):
    """
    Create a chart showing study progress over time.

    Args:
        study_df: DataFrame containing study log data
        daily_target: Daily study target in minutes (default: dynamically calculated)

    Returns:
        plotly.graph_objects.Figure: Study progress chart
    """
    # If daily_target is None, calculate it dynamically
    if daily_target is None:
        config = get_config()
        manual_override = config.get('study_tracking', {}).get('daily_target_minutes', 0)
        if manual_override > 0:
            daily_target = manual_override
        else:
            total_target_hours = config.get('study_tracking', {}).get('total_target_hours', 300)
            daily_target = calculate_daily_target(total_target_hours)

    study_df['date'] = pd.to_datetime(study_df['date'])
    study_by_date = study_df.groupby(study_df['date'].dt.date)['duration'].sum().reset_index()
    study_by_date.columns = ['Date', 'Minutes']

    # Get the date range for the last 30 days
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=29)

    # Create a date range with all dates
    date_range = pd.date_range(start=start_date, end=end_date)
    complete_study_df = pd.DataFrame({'Date': date_range})
    complete_study_df['Date'] = complete_study_df['Date'].dt.date

    # Merge with actual data and fill missing values
    study_by_date = pd.merge(complete_study_df, study_by_date, on='Date', how='left').fillna(0)

    # Mark which days met the target
    study_by_date['Target Met'] = study_by_date['Minutes'] >= daily_target

    # Create the chart with new color scheme
    fig = go.Figure()

    # Add target line
    fig.add_trace(go.Scatter(
        x=study_by_date['Date'],
        y=[daily_target] * len(study_by_date),
        mode='lines',
        name=f'Target ({daily_target} min)',
        line=dict(color=COLOR_ACCENT, width=2, dash='dash')
    ))

    # Add bars for study time with updated colors
    fig.add_trace(go.Bar(
        x=study_by_date['Date'],
        y=study_by_date['Minutes'],
        name='Study Minutes',
        marker_color=study_by_date['Target Met'].map({True: COLOR_SUCCESS, False: COLOR_PRIMARY})
    ))

    # Calculate 7-day moving average
    study_by_date['7-Day Avg'] = study_by_date['Minutes'].rolling(window=7, min_periods=1).mean()

    # Add moving average line
    fig.add_trace(go.Scatter(
        x=study_by_date['Date'],
        y=study_by_date['7-Day Avg'],
        mode='lines',
        name='7-Day Average',
        line=dict(color=COLOR_SECONDARY, width=3)
    ))

    fig.update_layout(
        title='Daily Study Progress',
        xaxis_title='Date',
        yaxis_title='Minutes',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color=COLOR_TEXT)
        ),
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0.05)',
        font=dict(
            family="Courier New, monospace",
            color=COLOR_TEXT
        ),
        xaxis=dict(
            gridcolor=COLOR_PRIMARY,
            zerolinecolor=COLOR_PRIMARY
        ),
        yaxis=dict(
            gridcolor=COLOR_PRIMARY,
            zerolinecolor=COLOR_PRIMARY
        ),
        hovermode='x unified'
    )

    return fig


# Also update this function
def plot_weekly_study_progress(study_df, daily_target=None):
    """
    Create a chart showing weekly study progress.

    Args:
        study_df: DataFrame containing study log data
        daily_target: Daily study target in minutes (default: dynamically calculated)

    Returns:
        plotly.graph_objects.Figure: Weekly study progress chart
    """
    # If daily_target is None, calculate it dynamically
    if daily_target is None:
        config = get_config()
        manual_override = config.get('study_tracking', {}).get('daily_target_minutes', 0)
        if manual_override > 0:
            daily_target = manual_override
        else:
            total_target_hours = config.get('study_tracking', {}).get('total_target_hours', 300)
            daily_target = calculate_daily_target(total_target_hours)

    if study_df.empty:
        # Return empty figure if no data
        fig = go.Figure()
        fig.update_layout(
            title='Weekly Study Progress',
            xaxis_title='Week',
            yaxis_title='Minutes',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0.05)',
            font=dict(
                family="Courier New, monospace",
                color=COLOR_TEXT
            )
        )
        return fig

    # Create a copy to avoid modifying the original
    weekly_study = study_df.copy()

    # Extract week and year
    weekly_study['date'] = pd.to_datetime(weekly_study['date'])
    weekly_study['week'] = weekly_study['date'].dt.isocalendar().week
    weekly_study['year'] = weekly_study['date'].dt.isocalendar().year

    # Group by week and calculate total duration
    weekly_study = weekly_study.groupby(['year', 'week'])['duration'].sum().reset_index()

    # Create week labels
    weekly_study['week_label'] = weekly_study['year'].astype(str) + '-W' + weekly_study['week'].astype(str)

    # Calculate weekly target
    weekly_target = daily_target * 7

    # Determine if target was met
    weekly_study['target_met'] = weekly_study['duration'] >= weekly_target

    # Create the chart with new color scheme
    fig = go.Figure()

    # Add bars for weekly study time
    fig.add_trace(go.Bar(
        x=weekly_study['week_label'],
        y=weekly_study['duration'],
        marker_color=weekly_study['target_met'].map({True: COLOR_SUCCESS, False: COLOR_PRIMARY}),
        name='Study Minutes'
    ))

    # Add weekly target line
    fig.add_trace(go.Scatter(
        x=weekly_study['week_label'],
        y=[weekly_target] * len(weekly_study),
        mode='lines',
        name=f'Weekly Target ({weekly_target} min)',
        line=dict(color=COLOR_ACCENT, dash='dash')
    ))

    fig.update_layout(
        title='Weekly Study Progress',
        xaxis_title='Week',
        yaxis_title='Minutes',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color=COLOR_TEXT)
        ),
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0.05)',
        font=dict(
            family="Courier New, monospace",
            color=COLOR_TEXT
        ),
        xaxis=dict(
            gridcolor=COLOR_PRIMARY,
            zerolinecolor=COLOR_PRIMARY
        ),
        yaxis=dict(
            gridcolor=COLOR_PRIMARY,
            zerolinecolor=COLOR_PRIMARY
        ),
        hovermode='x unified'
    )

    return fig


def plot_weekly_study_progress(study_df, daily_target=70):
    """
    Create a chart showing weekly study progress.

    Args:
        study_df: DataFrame containing study log data
        daily_target: Daily study target in minutes (default: 70)

    Returns:
        plotly.graph_objects.Figure: Weekly study progress chart
    """
    if study_df.empty:
        # Return empty figure if no data
        fig = go.Figure()
        fig.update_layout(
            title='Weekly Study Progress',
            xaxis_title='Week',
            yaxis_title='Minutes',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0.05)',
            font=dict(
                family="Courier New, monospace",
                color=COLOR_TEXT
            )
        )
        return fig

    # Create a copy to avoid modifying the original
    weekly_study = study_df.copy()

    # Extract week and year
    weekly_study['date'] = pd.to_datetime(weekly_study['date'])
    weekly_study['week'] = weekly_study['date'].dt.isocalendar().week
    weekly_study['year'] = weekly_study['date'].dt.isocalendar().year

    # Group by week and calculate total duration
    weekly_study = weekly_study.groupby(['year', 'week'])['duration'].sum().reset_index()

    # Create week labels
    weekly_study['week_label'] = weekly_study['year'].astype(str) + '-W' + weekly_study['week'].astype(str)

    # Calculate weekly target
    weekly_target = daily_target * 7

    # Determine if target was met
    weekly_study['target_met'] = weekly_study['duration'] >= weekly_target

    # Create the chart with new color scheme
    fig = go.Figure()

    # Add bars for weekly study time
    fig.add_trace(go.Bar(
        x=weekly_study['week_label'],
        y=weekly_study['duration'],
        marker_color=weekly_study['target_met'].map({True: COLOR_SUCCESS, False: COLOR_PRIMARY}),
        name='Study Minutes'
    ))

    # Add weekly target line
    fig.add_trace(go.Scatter(
        x=weekly_study['week_label'],
        y=[weekly_target] * len(weekly_study),
        mode='lines',
        name=f'Weekly Target ({weekly_target} min)',
        line=dict(color=COLOR_ACCENT, dash='dash')
    ))

    fig.update_layout(
        title='Weekly Study Progress',
        xaxis_title='Week',
        yaxis_title='Minutes',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color=COLOR_TEXT)
        ),
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0.05)',
        font=dict(
            family="Courier New, monospace",
            color=COLOR_TEXT
        ),
        xaxis=dict(
            gridcolor=COLOR_PRIMARY,
            zerolinecolor=COLOR_PRIMARY
        ),
        yaxis=dict(
            gridcolor=COLOR_PRIMARY,
            zerolinecolor=COLOR_PRIMARY
        ),
        hovermode='x unified'
    )

    return fig