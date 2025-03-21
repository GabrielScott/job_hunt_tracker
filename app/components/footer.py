import streamlit as st


def display_footer():
    """
    Display a clean, professional footer with the app version and credits.
    """
    # Use custom HTML/CSS to create a professionally styled footer
    footer_html = """
    <div style="
        margin-top: 3rem;
        padding: 1rem;
        border: 2px solid #E5F77D;
        text-align: center;
    ">
        <div style="
            font-family: 'Courier New', monospace;
            color: #757761;
            font-size: 0.8rem;
        ">
            Job Hunt & Study Tracker v1.0.1 • Built with ❤️ and Streamlit
        </div>
    </div>
    """

    st.markdown(footer_html, unsafe_allow_html=True)