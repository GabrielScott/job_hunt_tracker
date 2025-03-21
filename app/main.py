import streamlit as st
import os
import sys

# Add the parent directory to sys.path to allow imports from the app package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils.database import init_db
from app.pages import dashboard, job_tracker, study_tracker, settings

# Set page configuration
st.set_page_config(
    page_title="Job Hunt & Study Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
init_db()

# Custom CSS for a cleaner look
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 4rem;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px;
        margin-right: 5px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4c78a8;
        color: white;
    }
    /* Custom sidebar styling */
    .css-1d391kg {
        padding-top: 1rem;
    }
    .sidebar-nav-button {
        width: 100%;
        text-align: left;
        padding: 0.75rem 1rem;
        margin: 0.2rem 0;
        border-radius: 0.3rem;
        background-color: transparent;
        border: none;
        color: #262730;
        font-size: 1rem;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .sidebar-nav-button:hover {
        background-color: rgba(151, 166, 195, 0.15);
    }
    .sidebar-nav-button-active {
        background-color: #4c78a8;
        color: white;
    }
    .sidebar-nav-button-active:hover {
        background-color: #3a6691;
    }
        /* Hide default Streamlit navigation */
    header {display: none !important;}
    .stApp > header {display: none !important;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Hide any navigation tabs that might be auto-generated */
    [data-testid="stSidebarNav"], 
    [data-testid="collapsedControl"],
    [data-baseweb="tab-list"],
    [data-baseweb="tab"] {
        display: none !important;
    }
    
    /* Ensure the sidebar is the only navigation */
    section[data-testid="stSidebar"] {
        display: block !important;
        visibility: visible !important;
    }
</style>
""", unsafe_allow_html=True)


# Main App
def main():
    # Sidebar navigation
    st.sidebar.title("Navigation")

    # Store the current page in session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Dashboard"

    # Create styled navigation buttons
    for page_name in ["Dashboard", "Job Applications", "Study Tracker", "Settings"]:
        # Determine if this button is active
        is_active = st.session_state.current_page == page_name
        active_class = "sidebar-nav-button-active" if is_active else ""

        # Create the button with the appropriate styling
        if st.sidebar.button(
                page_name,
                key=f"nav_{page_name}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
        ):
            st.session_state.current_page = page_name
            # No need for st.experimental_rerun() in newer Streamlit versions

    # Display page based on selection
    if st.session_state.current_page == "Dashboard":
        dashboard.show()
    elif st.session_state.current_page == "Job Applications":
        job_tracker.show()
    elif st.session_state.current_page == "Study Tracker":
        study_tracker.show()
    elif st.session_state.current_page == "Settings":
        settings.show()

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.info("Job Hunt & Study Tracker v1.0.0")


if __name__ == "__main__":
    main()