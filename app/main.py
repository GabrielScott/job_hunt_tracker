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
</style>
""", unsafe_allow_html=True)


# Main App
def main():
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Dashboard", "Job Applications", "Study Tracker", "Settings"]
    )

    # Display page based on selection
    if page == "Dashboard":
        dashboard.show()
    elif page == "Job Applications":
        job_tracker.show()
    elif page == "Study Tracker":
        study_tracker.show()
    elif page == "Settings":
        settings.show()

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.info("Job Hunt & Study Tracker v1.0.0")


if __name__ == "__main__":
    main()