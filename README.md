# Job Hunt & Study Tracker

A comprehensive Streamlit dashboard for tracking job applications and SOA study progress. This application helps you manage your job search process and maintain consistency in your studies.

## Features

### Job Hunt Tracking
- 📝 Quickly add details of jobs you've applied for
- 📊 Track the status of each application (Applied, Screening, Interview, etc.)
- 📁 Upload and store resumes and cover letters for each position
- 📈 Visualize application trends and status distribution

### Study Progress Tracking
- ⏱️ Log daily study time for SOA exam preparation
- 🎯 Track progress against your daily target (1hr 10min)
- 📊 View daily and weekly study trends
- 🔥 Monitor your study streak

### Dashboard
- 📊 Overview of key metrics
- 💬 Motivational affirmations based on your progress
- 📈 Visual representations of your job hunt and study journey

## Installation

### Prerequisites
- Python 3.8 or higher
- Git

### Setup Instructions

1. Clone the repository
```bash
git clone https://github.com/yourusername/job-hunt-tracker.git
cd job-hunt-tracker
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the application
```bash
streamlit run app/main.py
```

The application will open in your default web browser at `http://localhost:8501`.

## Project Structure

```
job_hunt_tracker/
│
├── app/                  # Main application code
│   ├── main.py           # Entry point for the Streamlit application
│   ├── pages/            # Different pages of the Streamlit app
│   ├── components/       # Reusable UI components
│   └── utils/            # Utility functions
│
├── data/                 # Directory for storing database and files
│   ├── database/         # Where the SQLite database will be stored
│   └── uploads/          # Directory for uploaded files
│
├── tests/                # Test files
│
├── config/               # Configuration files
│
├── .gitignore            # Git ignore file
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Usage

### Job Applications Tracker
1. Navigate to the "Job Applications" page
2. Use the "Add New Application" tab to enter details about a job you've applied for
3. Upload your resume and cover letter for each position
4. Update the status of your applications as you progress through the hiring process

### Study Tracker
1. Navigate to the "Study Tracker" page
2. Log your daily study time for SOA exam preparation
3. Add notes about what topics you covered
4. Monitor your progress against your daily target of 1hr 10min

### Dashboard
- The main dashboard provides an overview of your job hunt and study progress
- View metrics, charts, and recent activities
- Get motivational affirmations based on your progress

## Customization

You can customize various aspects of the application by modifying the configuration file located at `config/app_config.json`:

- Change the daily study target
- Adjust the weekly application goal
- Modify status options for job applications
- Configure file storage locations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.