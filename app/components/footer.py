# app/components/footer.py
import streamlit as st

#Updated footer to cursor inspired layout
def display_footer():
    """
    Display an enhanced footer with animation effects.
    """
    # Define CSS for the enhanced footer
    footer_css = """
    <style>
    .enhanced-footer {
        margin-top: 3rem;
        padding: 1rem;
        border: 2px solid #E5F77D;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }

    .enhanced-footer:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(103, 89, 122, 0.1);
    }

    .footer-text {
        font-family: 'Courier New', monospace;
        color: #757761;
        font-size: 0.8rem;
        position: relative;
        z-index: 1;
    }

    .heart-icon {
        display: inline-block;
        color: #E9724C;
        transition: transform 0.3s ease;
    }

    .enhanced-footer:hover .heart-icon {
        transform: scale(1.3);
        animation: pulse 1s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.3); }
        100% { transform: scale(1); }
    }

    .enhanced-footer::before {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(229, 247, 125, 0.2), transparent);
        transition: left 0.5s ease;
    }

    .enhanced-footer:hover::before {
        left: 100%;
        transition: left 0.5s ease;
    }
    </style>
    """

    # Define the footer HTML content
    footer_html = """
    <div class="enhanced-footer">
        <div class="footer-text">
            Job Hunt & Study Tracker v1.0.1 • Built with <span class="heart-icon">❤️</span> and Streamlit
        </div>
    </div>
    """

    # Combine CSS and HTML
    st.markdown(footer_css + footer_html, unsafe_allow_html=True)