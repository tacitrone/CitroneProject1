import pytest
from unittest.mock import Mock, patch
from src.JobApplicationGUI import *

@pytest.fixture
def job_app(qapp):
    with patch('sqlite3.connect'):
        job_app = Mock(spec=JobInfoApp)
        job_app.fetch_jobs_data = JobInfoApp().fetch_jobs_data  # Use real method
        return job_app

def test_fetch_jobs_data(job_app):
    with patch('sqlite3.connect') as mock_connect:
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            (1, None, None, None, "Software Engineer", "Tech Co", "NY", "Full-time",
             "2025-01-01", "N/A", None, None, None, None, None, None, None, None,
             None, None, "Develop software solutions")
        ]
        mock_connect.return_value.cursor.return_value = mock_cursor
        jobs_data = job_app.fetch_jobs_data()
        assert len(jobs_data) == 1
        assert jobs_data[0]['title'] == "Software Engineer"
        assert jobs_data[0]['company'] == "Tech Co"
        assert jobs_data[0]['description'] == "Develop software solutions"
        mock_connect.assert_called_once_with("../resources/jobs.db")
        mock_cursor.execute.assert_called_once_with("SELECT * FROM jobs")