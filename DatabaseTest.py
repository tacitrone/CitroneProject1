import sqlite3
import pytest
from main import CREATE_TABLE_QUERY, insert_jobs

# Sample test job entry
TEST_JOB = [
    {
        "id": "test123",
        "site": "testsite",
        "job_url": "https://testsite.com/job123",
        "job_url_direct": "https://testsite.com/direct/job123",
        "title": "Test Job",
        "company": "Test Company",
        "location": "Test City, TC",
        "job_type": "fulltime",
        "date_posted": "2024-09-05",
        "salary_source": "direct_data",
        "interval": "yearly",
        "min_amount": 50000.0,
        "max_amount": 100000.0,
        "currency": "USD",
        "is_remote": "True",
        "job_level": "Entry",
        "job_function": "Engineering",
        "company_industry": "Tech",
        "listing_type": "Direct",
        "emails": "hr@testcompany.com",
        "description": "This is a test job description.",
        "company_url": "https://testcompany.com",
        "company_url_direct": "https://testcompany.com/careers",
        "company_addresses": "123 Test St, Test City",
        "company_num_employees": "100-500",
        "company_revenue": "10M-50M",
        "company_description": "A company that does test things.",
        "logo_photo_url": "",
        "banner_photo_url": "",
        "ceo_name": "John Doe",
        "ceo_photo_url": "",
    }
]


@pytest.fixture
def test_db():  # Create an in-memory database and set up the jobs table.
    conn = sqlite3.connect(":memory:")  # Create an in-memory database
    cursor = conn.cursor()

    # you were supposed to use your create table function - and test it
    # Create the jobs table
    cursor.execute(
        """
    CREATE TABLE jobs (
        id TEXT PRIMARY KEY,
        site TEXT,
        job_url TEXT,
        job_url_direct TEXT,
        title TEXT,
        company TEXT,
        location TEXT,
        job_type TEXT,
        date_posted TEXT,
        salary_source TEXT,
        interval TEXT,
        min_amount REAL,
        max_amount REAL,
        currency TEXT,
        is_remote TEXT,
        job_level TEXT,
        job_function TEXT,
        company_industry TEXT,
        listing_type TEXT,
        emails TEXT,
        description TEXT,
        company_url TEXT,
        company_url_direct TEXT,
        company_addresses TEXT,
        company_num_employees TEXT,
        company_revenue TEXT,
        company_description TEXT,
        logo_photo_url TEXT,
        banner_photo_url TEXT,
        ceo_name TEXT,
        ceo_photo_url TEXT
    );
    """
    )

    conn.commit()  # Ensure changes are saved

    yield conn  # Provide the connection to the test function

    conn.close()


def test_insert_and_verify_job(
    test_db,
):  # Test inserting a job and verifying its existence in the database.
    insert_jobs(TEST_JOB, test_db)  # Use test database connection

    # Query database for the test job
    cursor = test_db.cursor()
    cursor.execute(
        "SELECT id, title, company, location, min_amount, max_amount FROM jobs WHERE id = ?",
        ("test123",),
    )
    job = cursor.fetchone()

    assert job is not None, "Job should exist in the database"
    assert job[0] == "test123", "Job ID should match"
    assert job[1] == "Test Job", "Title should match"
    assert job[2] == "Test Company", "Company should match"
    assert job[3] == "Test City, TC", "Location should match"
    assert job[4] == 50000.0, "Min salary should match"
    assert job[5] == 100000.0, "Max salary should match"
