# app/components/section_manager.py

import streamlit as st
import pandas as pd
from datetime import datetime

from app.utils.database import get_db_connection


def get_study_sections():
    """Get all study sections with completion status."""
    conn = get_db_connection()

    sections_df = pd.read_sql('''
    SELECT id, name, description, completed, date_completed, order_num
    FROM study_sections
    ORDER BY order_num
    ''', conn)

    conn.close()
    return sections_df


def add_study_section(name, description, order_num):
    """Add a new study section."""
    conn = get_db_connection()
    c = conn.cursor()

    # Generate an ID based on the name
    section_id = f"section_{name.lower().replace(' ', '_')}"

    try:
        # Insert the new section
        c.execute(
            "INSERT INTO study_sections (id, name, description, order_num, completed) VALUES (?, ?, ?, ?, 0)",
            (section_id, name, description, order_num)
        )

        # Create an achievement for the section
        section_achievement_id = f"complete_{section_id}"
        c.execute(
            "INSERT INTO achievements (id, type, name, description, threshold, icon) VALUES (?, ?, ?, ?, ?, ?)",
            (section_achievement_id, "SECTION", f"Mastered: {name}",
             f"Complete the {name} section of the study manual", 1, "📚")
        )

        conn.commit()

        return True, "Section added successfully!"
    except Exception as e:
        conn.rollback()
        return False, f"Error adding section: {str(e)}"
    finally:
        conn.close()


def update_study_section(section_id, name, description, order_num):
    """Update an existing study section."""
    conn = get_db_connection()
    c = conn.cursor()

    try:
        # Update the section
        c.execute(
            "UPDATE study_sections SET name = ?, description = ?, order_num = ? WHERE id = ?",
            (name, description, order_num, section_id)
        )

        # Update the achievement name and description
        section_achievement_id = f"complete_{section_id}"
        c.execute(
            "UPDATE achievements SET name = ?, description = ? WHERE id = ?",
            (f"Mastered: {name}", f"Complete the {name} section of the study manual", section_achievement_id)
        )

        conn.commit()

        return True, "Section updated successfully!"
    except Exception as e:
        conn.rollback()
        return False, f"Error updating section: {str(e)}"
    finally:
        conn.close()


def delete_study_section(section_id):
    """Delete a study section."""
    conn = get_db_connection()
    c = conn.cursor()

    try:
        # Delete section achievement first
        section_achievement_id = f"complete_{section_id}"
        c.execute("DELETE FROM user_achievements WHERE achievement_id = ?", (section_achievement_id,))
        c.execute("DELETE FROM achievements WHERE id = ?", (section_achievement_id,))

        # Then delete the section
        c.execute("DELETE FROM study_sections WHERE id = ?", (section_id,))

        conn.commit()

        return True, "Section deleted successfully!"
    except Exception as e:
        conn.rollback()
        return False, f"Error deleting section: {str(e)}"
    finally:
        conn.close()


def display_section_manager():
    """Display the study section manager interface."""
    st.markdown("<h3 style='color: #67597A;'>Manage Study Manual Sections</h3>", unsafe_allow_html=True)

    # Get existing sections
    sections_df = get_study_sections()

    # Create tabs for different management functions
    tab1, tab2, tab3 = st.tabs(["View Sections", "Add Section", "Edit/Delete Sections"])

    with tab1:
        if not sections_df.empty:
            st.dataframe(
                sections_df[['name', 'description', 'completed', 'order_num']].rename(
                    columns={
                        'name': 'Section Name',
                        'description': 'Description',
                        'completed': 'Completed',
                        'order_num': 'Order'
                    }
                ),
                use_container_width=True
            )
        else:
            st.info("No study sections defined yet. Use the 'Add Section' tab to get started.")

    with tab2:
        st.markdown("<h4 style='color: #67597A;'>Add New Section</h4>", unsafe_allow_html=True)

        with st.form("add_section_form"):
            name = st.text_input("Section Name")
            description = st.text_area("Description")
            order_num = st.number_input("Order", min_value=1,
                                        value=len(sections_df) + 1 if not sections_df.empty else 1)

            submitted = st.form_submit_button("Add Section")

            if submitted:
                if not name:
                    st.error("Section name is required!")
                else:
                    success, message = add_study_section(name, description, order_num)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)

    with tab3:
        st.markdown("<h4 style='color: #67597A;'>Edit or Delete Sections</h4>", unsafe_allow_html=True)

        if sections_df.empty:
            st.info("No sections to edit. Add some sections first.")
        else:
            section_id = st.selectbox(
                "Select Section to Edit/Delete",
                options=sections_df['id'].tolist(),
                format_func=lambda x: sections_df.loc[sections_df['id'] == x, 'name'].values[0]
            )

            if section_id:
                selected_section = sections_df[sections_df['id'] == section_id].iloc[0]

                with st.form("edit_section_form"):
                    name = st.text_input("Section Name", value=selected_section['name'])
                    description = st.text_area("Description", value=selected_section['description'])
                    order_num = st.number_input("Order", min_value=1, value=selected_section['order_num'])

                    col1, col2 = st.columns(2)

                    with col1:
                        update_submitted = st.form_submit_button("Update Section")

                    with col2:
                        delete_submitted = st.form_submit_button("Delete Section", type="secondary")

                    if update_submitted:
                        if not name:
                            st.error("Section name is required!")
                        else:
                            success, message = update_study_section(section_id, name, description, order_num)
                            if success:
                                st.success(message)
                            else:
                                st.error(message)

                    if delete_submitted:
                        # Add confirmation
                        if st.checkbox("I confirm I want to delete this section"):
                            success, message = delete_study_section(section_id)
                            if success:
                                st.success(message)
                            else:
                                st.error(message)
                        else:
                            st.warning("Please confirm deletion.")


# Function to reset all sections to a predefined list
def reset_to_custom_sections():
    """Reset study sections to a custom list."""
    conn = get_db_connection()
    c = conn.cursor()

    # Custom study sections
    custom_sections = [
        {"id": "section_1", "name": "General Probability", "description": "Basic probability concepts and rules",
         "order": 1},
        {"id": "section_2", "name": "Univariate Distributions",
         "description": "Common distributions like Poisson & Exponential", "order": 2},
        {"id": "section_3", "name": "Multivariate Distributions",
         "description": "Conditional and marginal probabily functions", "order": 3},
        {"id": "section_4", "name": "Insurance and Risk Management",
         "description": "Basic insurance mechanics like deductibles, policy limits, and coinsurance.", "order": 4},
        {"id": "section_5", "name": "Review Section", "description": "Summary of all sections", "order": 5},
    ]

    try:
        # Delete existing section achievements
        c.execute("DELETE FROM achievements WHERE type = 'SECTION'")
        # Delete existing section completion records
        c.execute("DELETE FROM user_achievements WHERE achievement_id LIKE 'complete_section_%'")
        # Delete all study sections
        c.execute("DELETE FROM study_sections")

        # Insert the custom sections
        for section in custom_sections:
            c.execute(
                "INSERT INTO study_sections (id, name, description, order_num, completed) VALUES (?, ?, ?, ?, 0)",
                (section['id'], section['name'], section['description'], section['order'])
            )

            # Create an achievement for each section
            section_achievement_id = f"complete_{section['id']}"
            c.execute(
                "INSERT INTO achievements (id, type, name, description, threshold, icon) VALUES (?, ?, ?, ?, ?, ?)",
                (section_achievement_id, "SECTION", f"Mastered: {section['name']}",
                 f"Complete the {section['name']} section of the study manual", 1, "📚")
            )

        conn.commit()
        return True, "Study sections have been reset to your custom list!"

    except Exception as e:
        conn.rollback()
        return False, f"Error resetting study sections: {str(e)}"
    finally:
        conn.close()


def display_reset_button():
    """Display a button to reset sections to the custom list."""
    st.markdown("<h4 style='color: #67597A;'>Reset to Manual Sections</h4>", unsafe_allow_html=True)
    st.warning("This will delete all existing sections and replace them with your custom list.")

    if st.button("Reset to Custom Sections"):
        if st.checkbox("I confirm I want to reset all sections"):
            success, message = reset_to_custom_sections()
            if success:
                st.success(message)
            else:
                st.error(message)
        else:
            st.warning("Please confirm reset operation.")