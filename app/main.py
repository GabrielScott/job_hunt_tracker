import streamlit as st
import os
import sys

# Add the parent directory to sys.path to allow imports from the app package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils.database import init_db
from app.utils.achievements import init_achievements_db
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

# Initialize achievements database
init_achievements_db()

# Custom CSS for updated styling with new design kind of taking influence from cursor.com
st.markdown("""
<style>
    /* Import Google Font - Courier Prime (serif) */
    @import url('https://fonts.googleapis.com/css2?family=Courier+Prime:wght@400;700&display=swap');

    /* Global font styles */
    * {
        font-family: 'Courier Prime', monospace !important;
    }
    /* More visible grid with explicit container */
    .main .block-container::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
        
        /* Create a more visible grid pattern */
        background-image: 
            linear-gradient(rgba(255, 255, 255, 0.2) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.2) 1px, transparent 1px);
        background-size: 40px 40px;
        background-position: 0 0;
        background-color: rgba(244, 247, 190, 0.05);
    }
    
    /* Make sure there's no conflict with other containers */
    .main .block-container {
        position: relative;
        z-index: 1;
        background-color: transparent !important;
    }

    /* Button styling - square edges */
    .stButton button {
        background-color: #F4F7BE;
        color: #67597A;
        border: none;
        border-radius: 0 !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        position: relative;
        overflow: hidden;
    }

    .stButton button:hover {
        background-color: #E9724C;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    .stButton button:after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 5px;
        height: 5px;
        background: rgba(255, 255, 255, 0.5);
        opacity: 0;
        border-radius: 100%;
        transform: scale(1, 1) translate(-50%);
        transform-origin: 50% 50%;
    }

    .stButton button:hover:after {
        animation: ripple 1s ease-out;
    }

    @keyframes ripple {
        0% {
            transform: scale(0, 0);
            opacity: 0.5;
        }
        100% {
            transform: scale(20, 20);
            opacity: 0;
        }
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
        transition: all 0.3s ease;
    }

    .stTextInput input:focus, 
    .stTextArea textarea:focus,
    .stSelectbox:focus > div > div,
    .stNumberInput input:focus,
    .stDateInput input:focus {
        border-color: #E9724C !important;
        box-shadow: 0 0 0 2px rgba(233, 114, 76, 0.2);
        transform: translateY(-1px);
    }

    /* Dropdown menus */
    [data-baseweb="popover"] {
        border-radius: 0 !important;
    }

    /* Ensure tab text is always readable */
    .stTabs [data-baseweb="tab-list"] [data-baseweb="tab"][aria-selected="true"] {
        background-color: #67597A !important;
        color: #F4F7BE !important;
    }

    .stTabs [data-baseweb="tab-list"] [data-baseweb="tab"] {
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab-list"] [data-baseweb="tab"]:hover:not([aria-selected="true"]) {
        background-color: rgba(103, 89, 122, 0.1) !important;
        transform: translateY(-2px);
    }

    /* Fix for sidebar navigation buttons */
    .sidebar-nav-button-active {
        background-color: #E9724C !important;
        color: white !important;
        border-left-color: #F4F7BE !important;
    }

    /* Metrics styling */
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: bold;
        color: #E9724C;
        transition: all 0.3s ease;
    }

    div[data-testid="stMetricValue"]:hover {
        transform: scale(1.05);
        color: #67597A;
    }

    div[data-testid="stMetricLabel"] {
        color: #757761;
    }

    /* Common text styles */
    .header-text {
        color: #67597A;
        border-bottom: 2px solid #E5F77D;
        padding-bottom: 5px;
    }

    .label-text {
        color: #67597A; 
        font-weight: bold;
    }

    .content-text {
        color: #67597A;
    }

    /* Expander styling - square edges */
    .stExpander {
        border: 2px solid #E5F77D !important;
        border-radius: 0 !important;
        overflow: hidden;
        transition: all 0.3s ease;
    }

    .stExpander:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(103, 89, 122, 0.1);
        border-color: #E9724C !important;
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
        transition: all 0.3s ease;
    }

    .stExpander:hover summary {
        background-color: #E9724C;
        color: white;
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
        transition: all 0.3s ease;
    }

    .sidebar-nav-button:hover {
        background-color: #E9724C;
        border-left-color: #F4F7BE;
        transform: translateX(3px);
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
        transition: width 0.8s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }

    .stProgress > div {
        border-radius: 0 !important;
    }

    /* Message containers - square edges */
    .stInfo, .stSuccess, .stWarning, .stError {
        border-radius: 0 !important;
        padding: 1rem;
        border-left: 4px solid;
        transition: all 0.3s ease;
    }

    .stInfo:hover, .stSuccess:hover, .stWarning:hover, .stError:hover {
        transform: translateX(3px);
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

    /* Improve Status History visibility */
    .stInfo {
        background-color: #F4F7BE;
        color: #67597A !important;  /* Use purple for better visibility */
        border-left-color: #E5F77D;
        font-weight: 500;
    }

    /* Make sure all text in info boxes is visible */
    .stInfo * {
        color: #67597A !important;
    }


    /* Enhanced error text fixes with higher specificity */
    .stError,
    .stError p, 
    .stError div, 
    .stError span, 
    .stError code, 
    .stError pre {
        color: #67597A !important;
        font-weight: 500 !important;
    }

    /* Target Streamlit's exception elements specifically */
    [data-testid="stException"] {
        color: #67597A !important;
        font-weight: 500 !important;
        background-color: rgba(244, 247, 190, 0.7) !important;
        border-left: 4px solid #E9724C !important;
    }

    [data-testid="stException"] * {
        color: #67597A !important;
        font-weight: 500 !important;
    }

    /* Fix any other notification elements */
    .element-container .stNotification {
        color: #67597A !important;
        font-weight: 500 !important;
    }

    .element-container .stNotification * {
        color: #67597A !important;
        font-weight: 500 !important;
    }

    /* Any other text that might need fixing */
    .stAlert {
        color: #67597A !important;
    }

    .stAlert * {
        color: #67597A !important;
    }

    /* Data frames */
    [data-testid="stDataFrame"] table {
        border: 2px solid #E5F77D;
        transition: all 0.3s ease;
    }

    [data-testid="stDataFrame"] table:hover {
        border-color: #E9724C;
        box-shadow: 0 5px 15px rgba(103, 89, 122, 0.1);
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

    /* Achievement notification styling */
    .achievement-notification {
        animation: glow 1.5s infinite alternate;
        border: 2px solid #59A14F;
    }

    @keyframes glow {
        from {
            box-shadow: 0 0 5px #E5F77D;
        }
        to {
            box-shadow: 0 0 20px #E5F77D;
        }
    }

    /* Cursor.com inspired loading animation */
    @keyframes cursor-pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(103, 89, 122, 0.4);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(103, 89, 122, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(103, 89, 122, 0);
        }
    }

    .stApp::before {
        content: "";
        display: none;
        position: fixed;
        top: 10px;
        right: 10px;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background-color: #67597A;
        z-index: 9999;
        animation: cursor-pulse 2s infinite;
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .stApp.running::before {
        display: block;
        opacity: 1;
    }

    /* ============================================================= */
    /* ADD THE GRID TEXTURE CODE BELOW THIS LINE */
    /* ============================================================= */

    /* Grid background with parallax effect */
    body::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 0;
        pointer-events: none;

        /* Create a subtle grid pattern with white lines */
        background-image: 
            linear-gradient(rgba(255, 255, 255, 0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.1) 1px, transparent 1px);
        background-size: 40px 40px;

        /* Add a very subtle texture */
        background-color: rgba(244, 247, 190, 0.03);

        /* Initial transform for the parallax effect */
        transform: translateY(0);
        will-change: transform;
    }

    /* Enhanced spatial effects */
    .main .block-container {
        position: relative;
    }

    /* Add depth layers to create a subtle sense of space */
    .stTabs, .stExpander, .stMetric, .stDataFrame, .animated-header, .enhanced-footer {
        position: relative;
        z-index: 2;
        backdrop-filter: blur(0px); /* Initial state */
        transition: all 0.3s ease, backdrop-filter 0.5s ease;
    }

    /* Add subtle ambient movement to the UI */
    @keyframes ambient-shift {
        0% { transform: translate(0, 0); }
        25% { transform: translate(-0.5px, 0.5px); }
        50% { transform: translate(0.5px, 0.5px); }
        75% { transform: translate(0.5px, -0.5px); }
        100% { transform: translate(0, 0); }
    }

    /* Apply subtle ambient animation to certain elements */
    .stMetric, .stExpander {
        animation: ambient-shift 10s infinite ease-in-out;
    }

    /* Create a subtle light reflection effect on elements */
    .stExpander::before, .animated-header::before, .stMetric::before {
        content: "";
        position: absolute;
        top: -100%;
        left: -100%;
        width: 50%;
        height: 50%;
        background: linear-gradient(
            135deg, 
            rgba(255,255,255,0) 0%,
            rgba(255,255,255,0.03) 50%,
            rgba(255,255,255,0) 100%
        );
        transform: rotate(45deg);
        pointer-events: none;
        transition: all 1s ease;
        z-index: 2;
        opacity: 0;
    }

    /* Activate the light reflection effect on hover */
    .stExpander:hover::before, .animated-header:hover::before, .stMetric:hover::before {
        top: 120%;
        left: 120%;
        opacity: 1;
    }

    /* Create subtle noise texture */
    .main .block-container::after {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        opacity: 0.015;
        z-index: -1;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
    }

    /* Mouse movement tracking for subtle UI reaction */
    .stApp {
        --mouse-x: 0;
        --mouse-y: 0;
    }

    /* When in dark mode, adjust the grid opacity */
    @media (prefers-color-scheme: dark) {
        body::before {
            background-image: 
                linear-gradient(rgba(255, 255, 255, 0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 255, 255, 0.05) 1px, transparent 1px);
            background-color: rgba(0, 0, 0, 0.02);
        }
    }

    /* Animate elements when they enter the viewport */
    .stExpander, .stMetric, .stDataFrame {
        opacity: 0.95;
        transform: translateY(5px);
        transition: opacity 0.5s ease, transform 0.5s ease;
    }

    .stExpander.in-view, .stMetric.in-view, .stDataFrame.in-view {
        opacity: 1;
        transform: translateY(0);
    }

    /* Update the grid to incorporate mouse movement */
    body::before {
        transition: transform 0.2s ease-out;
    }
</style>

<script>
    // Add this JavaScript to detect when the app is loading
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.addedNodes.length && mutation.addedNodes[0].classList) {
                if (mutation.addedNodes[0].classList.contains('stProgress')) {
                    document.querySelector('.stApp').classList.add('running');
                }
            }
            if (mutation.removedNodes.length && mutation.removedNodes[0].classList) {
                if (mutation.removedNodes[0].classList.contains('stProgress')) {
                    document.querySelector('.stApp').classList.remove('running');
                }
            }
        });
    });

    // Start observing once the DOM is loaded
    document.addEventListener('DOMContentLoaded', function() {
        observer.observe(document.body, { childList: true, subtree: true });

        // ============================================================= */
        /* ADD THE MOUSE TRACKING SCRIPT BELOW THIS LINE */
        /* ============================================================= */

        // Track mouse movement for subtle UI reactions
        document.addEventListener('mousemove', function(e) {
            // Calculate mouse position relative to viewport
            const mouseX = e.clientX / window.innerWidth;
            const mouseY = e.clientY / window.innerHeight;

            // Update CSS variables for mouse position
            document.documentElement.style.setProperty('--mouse-x', mouseX);
            document.documentElement.style.setProperty('--mouse-y', mouseY);

            // Apply subtle transforms to elements based on mouse position
            const cards = document.querySelectorAll('.stExpander, .animated-header, .stMetric');
            cards.forEach(card => {
                if (card) {
                    const rect = card.getBoundingClientRect();

                    // Check if mouse is near the card
                    const cardCenterX = rect.left + rect.width / 2;
                    const cardCenterY = rect.top + rect.height / 2;

                    // Calculate distance from mouse to card center
                    const distX = (e.clientX - cardCenterX) / window.innerWidth;
                    const distY = (e.clientY - cardCenterY) / window.innerHeight;

                    // Only apply effect if mouse is relatively close
                    const distance = Math.sqrt(distX * distX + distY * distY);
                    if (distance < 0.2) {
                        // Calculate rotation based on mouse position
                        const rotateX = distY * 1.5; // Max 1.5 degrees
                        const rotateY = -distX * 1.5; // Max 1.5 degrees

                        // Apply subtle rotation
                        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
                    } else {
                        // Reset transform when mouse is far
                        card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0)';
                    }
                }
            });

            // Apply subtle movement to grid based on mouse
            const gridMovement = 5; // Max 5px movement
            document.body.style.setProperty('--grid-x-offset', `${(mouseX - 0.5) * -gridMovement}px`);
            document.body.style.setProperty('--grid-y-offset', `${(mouseY - 0.5) * -gridMovement}px`);

            // Update the grid transform with mouse position
            const style = document.createElement('style');
            style.textContent = `
                body::before { 
                    transform: translateX(var(--grid-x-offset, 0)) translateY(calc(var(--grid-y-offset, 0) + var(--scroll-y, 0) * 0.1px)); 
                }
            `;

            // Replace any existing mouse-tracking style
            const existingStyle = document.getElementById('mouse-tracking-style');
            if (existingStyle) {
                existingStyle.remove();
            }

            style.id = 'mouse-tracking-style';
            document.head.appendChild(style);
        });

        // Enable subtle parallax effect on scroll
        const parallaxItems = document.querySelectorAll('.animated-header, .enhanced-footer');
        window.addEventListener('scroll', function() {
            // Update scroll position CSS variable
            document.documentElement.style.setProperty('--scroll-y', window.scrollY);

            parallaxItems.forEach(item => {
                const scrollPosition = window.scrollY;
                const scrollFactor = item.classList.contains('animated-header') ? 0.4 : 0.2;
                const translateY = scrollPosition * scrollFactor;
                item.style.transform = `translateY(${translateY}px)`;
            });
        });

        // Detect when elements enter viewport for subtle entrance animations
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('in-view');
                }
            });
        }, { threshold: 0.1 });

        // Observe elements that should animate on scroll
        document.querySelectorAll('.stExpander, .stMetric, .stDataFrame').forEach(el => {
            observer.observe(el);
        });

        // Parallax grid scroll effect
        window.addEventListener('scroll', function() {
            const scrollY = window.scrollY;

            // Apply the custom property in the ::before pseudo element
            const style = document.createElement('style');
            style.textContent = `body::before { transform: translateY(${scrollY * 0.1}px); }`;

            // Replace any existing style element
            const existingStyle = document.getElementById('parallax-style');
            if (existingStyle) {
                existingStyle.remove();
            }

            style.id = 'parallax-style';
            document.head.appendChild(style);
        });
    });
</script>
""", unsafe_allow_html=True)
#Explicit Grid Creation
st.markdown("""
<div class="grid-background"></div>
<style>
.grid-background {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
    pointer-events: none;
    background-image: 
        linear-gradient(rgba(233, 114, 76, 0.2) 1px, transparent 1px),
        linear-gradient(90deg, rgba(233, 114, 76, 0.2) 1px, transparent 1px);
    background-size: 40px 40px;
    background-color: rgba(244, 247, 190, 0.05);
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