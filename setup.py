from setuptools import setup, find_packages

setup(
    name="job_hunt_tracker",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit>=1.23.0",
        "pandas>=1.5.0",
        "numpy>=1.23.0",
        "plotly>=5.13.0",
        "SQLAlchemy>=2.0.0",
        "xlsxwriter>=3.0.0",
    ],
    python_requires='>=3.8',
    author="Your Name",
    author_email="your.email@example.com",
    description="A Streamlit dashboard for tracking job applications and study progress",
    keywords="job hunting, study tracker, dashboard, streamlit",
    url="https://github.com/yourusername/job-hunt-tracker",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    entry_points={
        'console_scripts': [
            'job-hunt-tracker=app.main:main',
        ],
    },
)