import streamlit as st


def display_header():
    """
    Display a clean, professional header with the app name.
    """
    # Use custom HTML/CSS to create a more professionally styled header
    header_html = """
    <div style="
        border: 2px solid #E5F77D; 
        padding: 1.5rem; 
        margin-bottom: 1rem;
        text-align: center;
    ">
        <div style="
            font-family: 'Courier New', monospace; 
            font-size: 2.5rem; 
            font-weight: bold; 
            color: #67597A;
            letter-spacing: 2px;
            margin-bottom: 0.5rem;
        ">
            Job Hunt & Study Tracker
        </div>
        <div style="
            font-family: 'Courier New', monospace; 
            font-size: 1.2rem; 
            color: #757761;
            letter-spacing: 1px;
        ">
            Track your progress. Achieve your goals.
        </div>
    </div>
    """

    st.markdown(header_html, unsafe_allow_html=True)