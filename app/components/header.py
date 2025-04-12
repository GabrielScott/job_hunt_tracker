# app/components/header.py
import streamlit as st

#Updated Header for new cursor inspired design
def display_header():
    """
    Display an enhanced header with no border by default,
    that shows border and fills with gradient on hover.
    """
    # Add the CSS for the animated header
    st.markdown("""
    <style>
    .animated-header {
        border: 2px solid transparent; /* Start with transparent border */
        padding: 1.5rem;
        margin-bottom: 1rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: all 0.5s ease;
        background: transparent;  /* Start transparent */
        cursor: pointer;
    }

    .animated-header:hover {
        border: 2px solid transparent; /* Force all transparent */
        background: linear-gradient(120deg, rgba(234, 190, 247, 0.5), rgba(229, 247, 125, 0.8), rgba(244, 247, 190, 0.5));
        background-size: 200% 100%;
        animation: gradient-shift 3s ease infinite;
        transform: translateY(-2px);
        box-shadow: 0 10px 10px rgba(103, 89, 122, 0.1);
    }

    @keyframes gradient-shift {
        0% { background-position: 0% 50% }
        50% { background-position: 100% 50% }
        100% { background-position: 0% 50% }
    }

    .app-title {
        font-family: 'Courier New', monospace;
        font-size: 2.5rem;
        font-weight: bold;
        color: #FFFFF;
        letter-spacing: 2px;
        margin-bottom: 0.5rem;
        position: relative;
        display: inline-block;
    }

    .app-title:after {
        content: '';
        position: absolute;
        width: 0;
        height: 3px;
        bottom: 0;
        left: 0;
        background-color: #E9724C;
        transition: width 0.3s ease;
    }

    .animated-header:hover .app-title:after {
        width: 100%;
        
    }

    .app-subtitle {
        font-family: 'Courier New', monospace;
        font-size: 1.2rem;
        color: #757761;
        letter-spacing: 1px;
        transition: transform 0.3s ease, color 0.3s ease;
    }

    .animated-header:hover .app-subtitle {
        transform: translateY(2px);
        color: #67597A;
    }

    .icon-container {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 0.5rem;
    }

    .header-icon {
        font-size: 1.5rem;
        opacity: 0.7;
        transition: all 0.3s ease;
        color: #67597A;
    }

    .animated-header:hover .header-icon {
        transform: translateY(-3px);
        opacity: 1;
    }

    .header-icon:nth-child(1) { transition-delay: 0.1s; }
    .header-icon:nth-child(2) { transition-delay: 0.2s; }
    .header-icon:nth-child(3) { transition-delay: 0.3s; }

    /* Glow effect on hover */
    @keyframes glow-pulse {
        0% { box-shadow: 0 0 5px rgba(229, 247, 125, 0.1); }
        50% { box-shadow: 0 0 15px rgba(229, 247, 125, 0.3); }
        100% { box-shadow: 0 0 5px rgba(229, 247, 125, 0.1); }
    }

    .animated-header:hover {
        animation: glow-pulse 2s infinite;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header HTML with icons
    header_html = """
    <div class="animated-header">
        <div class="app-title">Job Hunt & Study Tracker</div>
        <div class="app-subtitle">Track your progress. Achieve your goals.</div>
        <div class="icon-container">
            <div class="header-icon">📊</div>
            <div class="header-icon">📝</div>
            <div class="header-icon">📚</div>
        </div>
    </div>
    """

    st.markdown(header_html, unsafe_allow_html=True)