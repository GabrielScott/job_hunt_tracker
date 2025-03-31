# app/components/achievements.py

import streamlit as st
import pandas as pd
from datetime import datetime

from app.utils.achievements import (
    get_all_achievements,
    get_unlocked_achievements,
    get_study_sections,
    mark_section_completed,
    mark_section_incomplete,
    check_for_achievements,
    get_achievement_by_id
)


def display_achievements():
    """Display all achievements with their status."""
    st.markdown("<h3 style='color: #67597A;'>SOA Exam P Achievements</h3>", unsafe_allow_html=True)

    # Get achievements
    achievements_df = get_all_achievements()

    if achievements_df.empty:
        st.info("No achievements defined yet.")
        return

    # Group by type
    achievement_types = {
        "STUDY_TIME": "Study Time Milestones",
        "STREAK": "Study Streaks",
        "SECTION": "Study Manual Sections"
    }

    for achievement_type, type_name in achievement_types.items():
        type_achievements = achievements_df[achievements_df['type'] == achievement_type]

        if not type_achievements.empty:
            st.markdown(f"<h4 style='color: #67597A;'>{type_name}</h4>", unsafe_allow_html=True)

            # Create a grid layout for achievements
            cols_per_row = 3
            for i in range(0, len(type_achievements), cols_per_row):
                cols = st.columns(cols_per_row)

                for j in range(cols_per_row):
                    if i + j < len(type_achievements):
                        achievement = type_achievements.iloc[i + j]
                        with cols[j]:
                            display_achievement_card(achievement)


def display_achievement_card(achievement):
    """Display a single achievement card."""
    # Determine card style based on unlock status
    if achievement['unlocked']:
        bg_color = "#E5F77D"  # Bright lime - unlocked
        border_color = "#59A14F"  # Secondary color
        text_color = "#67597A"  # Deep purple
        opacity = "1"
    else:
        bg_color = "#F4F7BE"  # Light cream - locked
        border_color = "#757761"  # Olive gray
        text_color = "#757761"  # Olive gray
        opacity = "0.7"

    # Create card HTML
    card_html = f"""
    <div style="
        background-color: {bg_color};
        border: 2px solid {border_color};
        border-radius: 0;
        padding: 10px;
        margin-bottom: 10px;
        opacity: {opacity};
    ">
        <div style="font-size: 2rem; text-align: center;">{achievement['icon']}</div>
        <div style="font-weight: bold; color: {text_color}; text-align: center;">{achievement['name']}</div>
        <div style="color: {text_color}; font-size: 0.8rem; text-align: center;">{achievement['description']}</div>
    """

    # Add unlocked date if achievement is unlocked
    if achievement['unlocked']:
        unlocked_date = datetime.strptime(achievement['date_unlocked'], "%Y-%m-%d %H:%M:%S").strftime("%b %d, %Y")
        card_html += f"""
        <div style="
            background-color: {border_color};
            color: white;
            text-align: center;
            font-size: 0.7rem;
            padding: 2px;
            margin-top: 5px;
        ">
            Unlocked on {unlocked_date}
        </div>
        """

    card_html += "</div>"

    st.markdown(card_html, unsafe_allow_html=True)


def display_achievement_notification(achievement_id):
    """Display a notification for a newly unlocked achievement."""
    achievement = get_achievement_by_id(achievement_id)

    if achievement:
        notification_html = f"""
        <div style="
            background-color: #E5F77D;
            border: 2px solid #59A14F;
            padding: 15px;
            margin: 10px 0;
            text-align: center;
        ">
            <div style="font-size: 3rem;">{achievement['icon']}</div>
            <div style="font-weight: bold; color: #67597A; font-size: 1.2rem;">Achievement Unlocked!</div>
            <div style="font-weight: bold; color: #67597A;">{achievement['name']}</div>
            <div style="color: #757761;">{achievement['description']}</div>
        </div>
        """

        st.markdown(notification_html, unsafe_allow_html=True)

        # Add a small celebration effect - could be replaced with a more elaborate animation
        st.balloons()


def check_and_display_new_achievements():
    """Check for new achievements and display notifications."""
    # Check for new achievements
    newly_unlocked = check_for_achievements()

    # Display notifications for newly unlocked achievements
    for achievement_id in newly_unlocked:
        display_achievement_notification(achievement_id)

    return newly_unlocked


def display_study_sections():
    """Display study sections with completion tracking."""
    st.markdown("<h3 style='color: #67597A;'>SOA Exam P Study Manual Sections</h3>", unsafe_allow_html=True)

    # Get sections
    sections_df = get_study_sections()

    if sections_df.empty:
        st.info("No study sections defined yet.")
        return

    # Calculate overall progress
    completed_sections = sections_df['completed'].sum()
    total_sections = len(sections_df)
    progress_percentage = (completed_sections / total_sections) * 100 if total_sections > 0 else 0

    # Display progress bar
    st.progress(progress_percentage / 100)
    st.markdown(
        f"<div style='text-align: center; color: #67597A;'><b>Overall Progress:</b> {completed_sections}/{total_sections} sections completed ({progress_percentage:.1f}%)</div>",
        unsafe_allow_html=True)

    # Display each section
    for _, section in sections_df.iterrows():
        with st.expander(f"{section['name']} {'✅' if section['completed'] else ''}"):
            st.markdown(f"<div style='color: #67597A;'><b>Description:</b> {section['description']}</div>",
                        unsafe_allow_html=True)

            # Display completion date if completed
            if section['completed']:
                completion_date = datetime.strptime(section['date_completed'], "%Y-%m-%d %H:%M:%S").strftime(
                    "%b %d, %Y")
                st.markdown(f"<div style='color: #59A14F;'><b>Completed on:</b> {completion_date}</div>",
                            unsafe_allow_html=True)

                # Option to mark as incomplete
                if st.button("Mark as Incomplete", key=f"incomplete_{section['id']}"):
                    mark_section_incomplete(section['id'])
                    st.success(f"'{section['name']}' marked as incomplete.")
                    st.rerun()
            else:
                # Option to mark as completed
                if st.button("Mark as Completed", key=f"complete_{section['id']}"):
                    mark_section_completed(section['id'])
                    st.success(f"'{section['name']}' marked as completed!")
                    st.rerun()