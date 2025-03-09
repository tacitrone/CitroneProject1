import sys
import pytest
import sqlite3
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from src.JobApplicationGUI import JobInfoApp
from src.Functions import *

DB_FILE = "../resources/jobs.db"

@pytest.fixture(scope="session")
def app():
    """Ensure a single QApplication instance is created for all tests."""
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    yield app

@pytest.fixture
def job_info_app(app):
    """Create JobInfoApp instance after QApplication exists."""
    job_app = JobInfoApp()
    job_app.show()  # Show UI for testing
    yield job_app
    job_app.close()

@pytest.fixture
def db_connection():
    """Create and close a database connection for testing."""
    conn = sqlite3.connect(DB_FILE)
    yield conn
    conn.close()

@pytest.fixture
def setup_database(db_connection):
    """Set up and clean up the database before and after tests."""
    create_person_table()
    yield
    cursor = db_connection.cursor()
    cursor.execute("DELETE FROM person")  # Clean up after test
    db_connection.commit()

def test_show_job_details(job_info_app, qtbot):
    """Test that selecting a job updates the job details text correctly."""
    if not job_info_app.jobs_data:
        pytest.skip("No job data available for testing.")

    # Select the first job in the list
    qtbot.mouseClick(job_info_app.job_list_widget, Qt.LeftButton)
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

def test_insert_person_into_db(setup_database, db_connection):
    """Test that user-entered data is stored in the database correctly."""
    person = Person(
        "Test Profile", "John Doe", "25", "Test University", "3.8", "2 years",
        "Python, SQL", "Portfolio Project", "john@example.com", "1234567890",
        "linkedin.com/in/johndoe", "123 Test St", "CS101, CS202"
    )

    insert_person_into_db(person)

    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM person WHERE name = ?", ("John Doe",))
    result = cursor.fetchone()

    assert result is not None, "Person record was not inserted into the database."
    assert result[1:] == (
        "Test Profile", "John Doe", 25, "Test University", 3.8, "2 years",
        "Python, SQL", "Portfolio Project", "john@example.com", "1234567890",
        "linkedin.com/in/johndoe", "123 Test St", "CS101, CS202"
    )
