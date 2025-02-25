import pytest
import sqlite3
from PyQt5.QtWidgets import QApplication
from JobApplicationGUI import *
from Functions import *  # Assuming you have a Person model

DB_FILE = "jobs.db"


@pytest.fixture(scope="module")
def app():
    return QApplication([])


@pytest.fixture
def job_info_app(app):
    return JobInfoApp()


@pytest.fixture
def db_connection():
    conn = sqlite3.connect(DB_FILE)
    yield conn
    conn.close()


@pytest.fixture
def setup_database(db_connection):
    create_person_table()
    yield
    cursor = db_connection.cursor()
    cursor.execute("DELETE FROM person")  # Clean up after test
    db_connection.commit()


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


def test_insert_person_into_db(setup_database, db_connection):
    """Test that user-entered data is stored in the database correctly."""
    person = Person("John Doe", "25", "Test University", "3.8", "2 years", "Python, SQL", "Portfolio Project",
                    "john@example.com", "1234567890", "linkedin.com/in/johndoe", "123 Test St", "CS101, CS202")

    insert_person_into_db(person)

    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM person WHERE name = ?", ("John Doe",))
    result = cursor.fetchone()

    assert result is not None, "Person record was not inserted into the database."
    assert result[1] == "John Doe"
    assert str(result[2]) == "25"
    assert result[3] == "Test University"
    assert str(result[4]) == "3.8"
    assert result[5] == "2 years"
    assert result[6] == "Python, SQL"
    assert result[7] == "Portfolio Project"
    assert result[8] == "john@example.com"
    assert result[9] == "1234567890"
    assert result[10] == "linkedin.com/in/johndoe"
    assert result[11] == "123 Test St"
    assert result[12] == "CS101, CS202"
