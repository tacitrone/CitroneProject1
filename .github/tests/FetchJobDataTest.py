import pytest
from unittest.mock import Mock, patch
from PyQt5.QtWidgets import QApplication
from JobApplicationGUI import *

# Fixture for QApplication (needed for PyQt5 tests)
@pytest.fixture
def app(qtbot):
    test_app = QApplication.instance()
    if test_app is None:
        test_app = QApplication([])
    yield test_app
    test_app.quit()

# Fixture to set up the JobInfoApp instance
@pytest.fixture
def job_app(app):
    with patch('sqlite3.connect'):  # Mock SQLite connection
        return JobInfoApp()



# Test 3: Test the fetch_jobs_data production function
def test_fetch_jobs_data(job_app):
    # Mock SQLite connection and cursor
    with patch('sqlite3.connect') as mock_connect:
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            (1, None, None, None, "Software Engineer", "Tech Co", "NY", "Full-time",
             "2025-01-01", "N/A", None, None, None, None, None, None, None, None,
             None, None, "Develop software solutions")
        ]
        mock_connect.return_value.cursor.return_value = mock_cursor

        # Call the function
        jobs_data = job_app.fetch_jobs_data()

        # Assertions
        assert len(jobs_data) == 1
        assert jobs_data[0]['title'] == "Software Engineer"
        assert jobs_data[0]['company'] == "Tech Co"
        assert jobs_data[0]['description'] == "Develop software solutions"
        mock_connect.assert_called_once_with("jobs.db")
        mock_cursor.execute.assert_called_once_with("SELECT * FROM jobs")
