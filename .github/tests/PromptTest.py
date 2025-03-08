import pytest
from unittest.mock import patch, MagicMock
from JobApplicationGUI import JobInfoApp  # Corrected module name
from PyQt5.QtWidgets import QApplication
import sys


@pytest.fixture(scope="session", autouse=True)
def qt_app():
    app = QApplication(sys.argv)
    yield app


@pytest.fixture
def mock_db_connection():
    with patch('JobApplicationGUI.sqlite3.connect') as mock_connect:  # Corrected path
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Mock profile data
        mock_cursor.fetchone.return_value = (
            1, "Test Profile", "John Doe", 25, "Test University", 3.8,
            "2 years of experience", "Python, Java", "Portfolio Project",
            "john@example.com", "1234567890", "linkedin.com/john", "123 Street", "CS101, AI"
        )

        yield mock_connect


@pytest.fixture
def job_info_app(mock_db_connection):
    app = JobInfoApp()

    # Mock GUI elements to prevent crashes
    app.profile_dropdown = MagicMock()
    app.job_list_widget = MagicMock()
    app.job_details_text = MagicMock()

    app.jobs_data = [{
        'title': 'Software Engineer',
        'company': 'Tech Corp',
        'location': 'New York',
        'job_type': 'Full-time',
        'date_posted': '2024-03-01',
        'salary_source': 'Glassdoor',
        'description': 'Looking for a software engineer with Python experience.'
    }]

    app.profile_dropdown.currentText.return_value = "Test Profile"
    app.job_list_widget.currentRow.return_value = 0
    app.job_details_text.toPlainText.return_value = "Generated Resume Text"

    return app


def test_create_resume_prompt_contains_profile_and_job_data(job_info_app):
    app = job_info_app

    app.create_resume()

    expected_profile_keywords = ["John Doe", "Test University", "Python, Java", "CS101, AI"]
    expected_job_keywords = ["Software Engineer", "Tech Corp", "Python experience"]

    resume_text = app.job_details_text.toPlainText()

    for keyword in expected_profile_keywords:
        assert keyword in resume_text, f"Missing profile data: {keyword}"

    for keyword in expected_job_keywords:
        assert keyword in resume_text, f"Missing job data: {keyword}"