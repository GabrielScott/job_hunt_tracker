import streamlit as st
import os
import sys

# Add the parent directory to sys.path to allow imports from the app package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils.database import init_db
from app.pages import dashboard, job_tracker, study_tracker, settings
from app.components.header import display_header
from app.components.footer import display_footer

# Set page configuration
st.set_page_config(
    page_title="Job Hunt & Study Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
init_db()

# Custom CSS for updated styling with new colors and font, square edges
st.markdown("""
<style>
    /* Import Google Font - Courier Prime (serif) */
    @import url('https://fonts.googleapis.com/css2?family=Courier+Prime:wght@400;700&display=swap');

    /* Global font styles */
    * {
        font-family: 'Courier Prime', monospace !important;
    }

    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Button styling - square edges */
    .stButton button {
        background-color: #67597A;
        color: #F4F7BE;
        border: none;
        border-radius: 0 !important;
        transition: all 0.3s;
    }

    .stButton button:hover {
        background-color: #E9724C;
        color: white;
    }

    /* Form elements - square edges */
    .stTextInput input, 
    .stTextArea textarea, 
    .stSelectbox > div > div, 
    .stNumberInput input, 
    .stDateInput input,
    .stDateInput > div,
    .stSelectbox > div,
    [data-baseweb="select"] {
        border-radius: 0 !important;
        border: 2px solid #E5F77D !important;
        color: #757761;
    }

    /* Dropdown menus */
    [data-baseweb="popover"] {
        border-radius: 0 !important;
    }

    /* Tab styling - square edges */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background-color: #F4F7BE;
        border: 2px solid #E5F77D;
    }

    .stTabs [data-baseweb="tab"] {
        height: 4rem;
        white-space: pre-wrap;
        background-color: #F4F7BE;
        border-radius: 0 !important;
        margin-right: 0;
        border-right: 2px solid #E5F77D;
        color: #67597A;
        font-weight: bold;
    }

    .stTabs [aria-selected="true"] {
        background-color: #67597A;
        color: #F4F7BE;
    }

    /* Metrics styling */
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: bold;
        color: #E9724C;
    }

    div[data-testid="stMetricLabel"] {
        color: #757761;
    }

    /* Expander styling - square edges */
    .stExpander {
        border: 2px solid #E5F77D !important;
        border-radius: 0 !important;
        overflow: hidden;
    }

    .stExpander details {
        background-color: #F4F7BE;
    }

    .stExpander summary {
        background-color: #E5F77D;
        color: #67597A;
        font-weight: bold;
        padding: 1rem;
        border-radius: 0 !important;
    }

    /* Remove all rounded corners */
    div, input, button, select, textarea, a {
        border-radius: 0 !important;
    }

    /* Custom sidebar styling - square edges */
    [data-testid="stSidebar"] {
        background-color: #67597A;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1 {
        color: #F4F7BE;
    }

    [data-testid="stSidebar"] .stInfo {
        background-color: #E9724C;
        color: white;
        border-radius: 0 !important;
    }

    .sidebar-nav-button {
        width: 100%;
        text-align: left;
        padding: 0.75rem 1rem;
        margin: 0.2rem 0;
        border-radius: 0 !important;
        background-color: transparent;
        border-left: 3px solid #E5F77D;
        color: #F4F7BE;
        font-size: 1rem;
        cursor: pointer;
        transition: background-color 0.3s;
    }

    .sidebar-nav-button:hover {
        background-color: #E9724C;
        border-left-color: #F4F7BE;
    }

    .sidebar-nav-button-active {
        background-color: #E9724C;
        color: white;
        border-left-color: #F4F7BE;
    }

    /* Progress bars - square edges */
    .stProgress > div > div {
        background-color: #E9724C;
        border-radius: 0 !important;
    }

    .stProgress > div {
        border-radius: 0 !important;
    }

    /* Message containers - square edges */
    .stInfo, .stSuccess, .stWarning, .stError {
        border-radius: 0 !important;
        padding: 1rem;
        border-left: 4px solid;
    }

    .stInfo {
        background-color: #F4F7BE;
        color: #757761;
        border-left-color: #E5F77D;
    }

    .stSuccess {
        background-color: #F4F7BE;
        color: #67597A;
        border-left-color: #E5F77D;
    }

    .stWarning {
        background-color: #F4F7BE;
        color: #E9724C;
        border-left-color: #E9724C;
    }

    .stError {
        background-color: #F4F7BE;
        color: #E9724C;
        border-left-color: #E9724C;
    }

    /* Data frames */
    [data-testid="stDataFrame"] table {
        border: 2px solid #E5F77D;
    }

    [data-testid="stDataFrame"] th {
        background-color: #67597A;
        color: #F4F7BE;
        font-family: 'Courier Prime', monospace !important;
    }

    [data-testid="stDataFrame"] td {
        font-family: 'Courier Prime', monospace !important;
    }

    /* Hide default Streamlit navigation */
    header {display: none !important;}
    .stApp > header {display: none !important;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Hide any navigation tabs that might be auto-generated */
    [data-testid="stSidebarNav"], 
    [data-testid="collapsedControl"] {
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
    # Clear sidebar of any auto-generated navigation
    st.sidebar.empty()

    # Add our custom navigation
    st.sidebar.title("Navigation")

    # Store the current page in session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Dashboard"

    # Create styled navigation buttons
    for page_name in ["Dashboard", "Job Applications", "Study Tracker", "Settings"]:
        # Determine if this button is active
        is_active = st.session_state.current_page == page_name

        # Create the button with the appropriate styling
        if st.sidebar.button(
                page_name,
                key=f"nav_{page_name}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
        ):
            st.session_state.current_page = page_name
            st.rerun()

    # Display the custom header
    display_header()

    # Display page based on selection
    if st.session_state.current_page == "Dashboard":
        dashboard.show()
    elif st.session_state.current_page == "Job Applications":
        job_tracker.show()
    elif st.session_state.current_page == "Study Tracker":
        study_tracker.show()
    elif st.session_state.current_page == "Settings":
        settings.show()

    # Display the custom footer
    display_footer()

    # Sidebar footer
    st.sidebar.markdown("---")
    st.sidebar.info("Job Hunt & Study Tracker v1.0.1")


if __name__ == "__main__":
    main()