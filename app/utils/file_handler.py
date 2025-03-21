import os
import base64
from datetime import datetime
from pathlib import Path
import shutil
from io import BytesIO

from app.utils.database import UPLOADS_PATH


def save_uploaded_file(uploaded_file, directory_name=None):
    """
    Save an uploaded file and return the saved file path.

    Args:
        uploaded_file: The uploaded file object from Streamlit
        directory_name: Optional subdirectory name within uploads folder

    Returns:
        str: Path to the saved file
    """
    if uploaded_file is None:
        return None

    # Generate a clean filename with timestamp to prevent overwriting
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{uploaded_file.name}"

    # Set up directory path
    if directory_name:
        directory = UPLOADS_PATH / directory_name
        directory.mkdir(exist_ok=True)
    else:
        directory = UPLOADS_PATH

    # Full path to save the file
    filepath = directory / filename

    # Save file
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return str(filepath)


def save_resume(uploaded_file, company, position):
    """
    Save a resume file with structured naming.

    Args:
        uploaded_file: The uploaded file object from Streamlit
        company: Company name for the resume
        position: Position name for the resume

    Returns:
        str: Path to the saved resume
    """
    if uploaded_file is None:
        return None

    # Clean company and position names for filename
    company_clean = "".join(c if c.isalnum() else "_" for c in company)
    position_clean = "".join(c if c.isalnum() else "_" for c in position)

    # Generate filename with company, position, and timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    extension = uploaded_file.name.split('.')[-1]
    filename = f"resume_{company_clean}_{position_clean}_{timestamp}.{extension}"

    # Set up directory path
    directory = UPLOADS_PATH / "resumes"
    directory.mkdir(exist_ok=True)

    # Full path to save the file
    filepath = directory / filename

    # Save file
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return str(filepath)


def save_cover_letter(uploaded_file, company, position):
    """
    Save a cover letter file with structured naming.

    Args:
        uploaded_file: The uploaded file object from Streamlit
        company: Company name for the cover letter
        position: Position name for the cover letter

    Returns:
        str: Path to the saved cover letter
    """
    if uploaded_file is None:
        return None

    # Clean company and position names for filename
    company_clean = "".join(c if c.isalnum() else "_" for c in company)
    position_clean = "".join(c if c.isalnum() else "_" for c in position)

    # Generate filename with company, position, and timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    extension = uploaded_file.name.split('.')[-1]
    filename = f"cover_{company_clean}_{position_clean}_{timestamp}.{extension}"

    # Set up directory path
    directory = UPLOADS_PATH / "cover_letters"
    directory.mkdir(exist_ok=True)

    # Full path to save the file
    filepath = directory / filename

    # Save file
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return str(filepath)


def get_file_download_link(file_path, file_name=None):
    """
    Create a download link for a file.

    Args:
        file_path: Path to the file
        file_name: Optional name to display for the file

    Returns:
        str: HTML link for downloading the file
    """
    if file_path and os.path.exists(file_path):
        with open(file_path, "rb") as f:
            bytes_data = f.read()

        # Use the original filename if none is provided
        if file_name is None:
            file_name = os.path.basename(file_path)

        b64 = base64.b64encode(bytes_data).decode()

        # Try to determine MIME type based on extension
        extension = file_path.split('.')[-1].lower()
        mime_type = "application/octet-stream"  # Default

        if extension == "pdf":
            mime_type = "application/pdf"
        elif extension in ["doc", "docx"]:
            mime_type = "application/msword"
        elif extension in ["xls", "xlsx"]:
            mime_type = "application/vnd.ms-excel"
        elif extension == "txt":
            mime_type = "text/plain"

        href = f'<a href="data:{mime_type};base64,{b64}" download="{file_name}">Download {file_name}</a>'
        return href

    return "No file available"


def export_dataframe(df, filename, format_type="csv"):
    """
    Export a dataframe to CSV or Excel.

    Args:
        df: Pandas DataFrame to export
        filename: Name for the exported file
        format_type: Either "csv" or "excel"

    Returns:
        str: HTML link for downloading the file
    """
    if format_type.lower() == "csv":
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Download CSV File</a>'
        return href

    elif format_type.lower() == "excel":
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Data', index=False)
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}.xlsx">Download Excel File</a>'
        return href

    return "Invalid format type"


def delete_file(file_path):
    """Delete a file if it exists."""
    if file_path and os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False