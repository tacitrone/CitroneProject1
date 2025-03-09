import pytest
from unittest.mock import Mock, patch
from src.Functions import fetch_jobs_data  # Adjust import based on your structure

def test_fetch_jobs_data():
    with patch('sqlite3.connect') as mock_connect:
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            (1, None, None, None, "Software Engineer", "Tech Co", "NY", "Full-time",
             "2025-01-01", "N/A", None, None, None, None, None, None, None, None,
             None, None, "Develop software solutions")
        ]
        mock_connect.return_value.cursor.return_value = mock_cursor
        jobs_data = fetch_jobs_data()
        assert len(jobs_data) == 1
        assert jobs_data[0]['title'] == "Software Engineer"
        assert jobs_data[0]['company'] == "Tech Co"
        assert jobs_data[0]['description'] == "Develop software solutions"
        mock_connect.assert_called_once_with("../resources/jobs.db")
        mock_cursor.execute.assert_called_once_with("SELECT * FROM jobs")