import pytest
from PyQt5.QtWidgets import QApplication
from JobApplicationGUI import * 

@pytest.fixture(scope="module")
def app():
    return QApplication([])

@pytest.fixture
def job_info_app(app):
    return JobInfoApp()

def test_show_job_details(job_info_app):
    """Test that selecting a job updates the job details text correctly."""
    if not job_info_app.jobs_data:
        pytest.skip("No job data available for testing.")

    # Select the first job in the list
    job_info_app.job_list_widget.setCurrentRow(0)
    job_info_app.show_job_details()

    # Get expected job details
    selected_job = job_info_app.jobs_data[0]
    expected_text = (
        f"Title: {selected_job['title']}\n"
        f"Company: {selected_job['company']}\n"
        f"Location: {selected_job['location']}\n"
        f"Job Type: {selected_job['job_type']}\n"
        f"Date Posted: {selected_job['date_posted']}\n"
        f"Salary Source: {selected_job['salary_source']}\n"
        f"\nDescription:\n{selected_job['description']}"
    )

    # Check if the job details text is correctly updated
    assert job_info_app.job_details_text.toPlainText() == expected_text
