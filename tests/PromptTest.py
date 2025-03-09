import pytest
from src.JobApplicationGUI import *
from src.Functions import *


# Mock class to simulate the 'self' parameter
class MockResumeGenerator:
    def __init__(self):
        pass


@pytest.fixture
def mock_generator():
    return MockResumeGenerator()


@pytest.fixture
def sample_person():
    return {
        "Profile": "Software Engineer",
        "Name": "John Doe",
        "Age": 30,
        "School": "Tech University",
        "GPA": 3.8,
        "Experience": "5 years",
        "Skills": "Python, Java, SQL",
        "Projects": "Project A, Project B",
        "Email": "john.doe@example.com",
        "Phone": "123-456-7890",
        "LinkedIn": "linkedin.com/in/johndoe",
        "Address": "123 Tech St",
        "Classes": "CS101, CS202",
        "EmptyField": ""  # This should be filtered out by printPerson
    }


@pytest.fixture
def sample_job():
    return {
        "description": "Looking for a skilled Software Engineer with experience in Python and Java."
    }


def test_createResumePrompt(mock_generator, sample_person, sample_job):
    # Call the function with mocked self
    prompt = createResumePrompt(mock_generator, sample_person, sample_job)

    # Expected parts of the prompt
    expected_start = "Give me a sample resume in markdown format designed for my skills and the job description I provided."
    expected_person = printPerson(sample_person)
    expected_job = sample_job["description"]

    # Assertions
    assert isinstance(prompt, str)
    assert expected_start in prompt
    assert expected_person in prompt
    assert expected_job in prompt
    assert "Here is a description of myself:" in prompt
    assert "Here is a job description:" in prompt
    assert "EmptyField" not in prompt  # Should be filtered out by printPerson


def test_createCoverLetterPrompt(mock_generator, sample_person, sample_job):
    # Call the function with mocked self
    prompt = createCoverLetterPrompt(mock_generator, sample_person, sample_job)

    # Expected parts of the prompt
    expected_start = "Give me a sample cover letter in markdown format designed for my skills and the job description I provided."
    expected_person = printPerson(sample_person)
    expected_job = sample_job["description"]

    # Assertions
    assert isinstance(prompt, str)
    assert expected_start in prompt
    assert expected_person in prompt
    assert expected_job in prompt
    assert "Here is a description of myself:" in prompt
    assert "Here is a job description:" in prompt
    assert "EmptyField" not in prompt  # Should be filtered out by printPerson


def test_prompts_differ(mock_generator, sample_person, sample_job):
    # Ensure resume and cover letter prompts are different
    resume_prompt = createResumePrompt(mock_generator, sample_person, sample_job)
    cover_prompt = createCoverLetterPrompt(mock_generator, sample_person, sample_job)

    assert resume_prompt != cover_prompt
    assert "resume" in resume_prompt.lower()
    assert "cover letter" in cover_prompt.lower()


def test_empty_person_data(mock_generator, sample_job):
    # Test with empty person data
    empty_person = {"Name": "", "Age": None, "Skills": 0}  # All falsy values
    resume_prompt = createResumePrompt(mock_generator, empty_person, sample_job)
    cover_prompt = createCoverLetterPrompt(mock_generator, empty_person, sample_job)

    # Split the prompt and check the person data section
    resume_person_section = resume_prompt.split("myself:")[1].split("Here is a job")[0].strip()
    cover_person_section = cover_prompt.split("myself:")[1].split("Here is a job")[0].strip()

    # Assert that the person section is empty (only whitespace or newlines)
    assert resume_person_section == ""  # Should be empty after strip()
    assert cover_person_section == ""
    # Ensure job description is still present
    assert sample_job["description"] in resume_prompt
    assert sample_job["description"] in cover_prompt


def test_partial_person_data(mock_generator, sample_job):
    # Test with some empty fields
    partial_person = {
        "Name": "Jane Doe",
        "Age": None,  # Falsy, should be filtered
        "Skills": "Python",
        "Experience": ""  # Falsy, should be filtered
    }
    resume_prompt = createResumePrompt(mock_generator, partial_person, sample_job)
    cover_prompt = createCoverLetterPrompt(mock_generator, partial_person, sample_job)

    person_text = printPerson(partial_person)
    assert "Name: Jane Doe" in person_text
    assert "Skills: Python" in person_text
    assert "Age" not in person_text
    assert "Experience" not in person_text
    assert person_text in resume_prompt
    assert person_text in cover_prompt
    assert sample_job["description"] in resume_prompt
    assert sample_job["description"] in cover_prompt


def test_empty_job_description(mock_generator, sample_person):
    # Test with empty job description
    empty_job = {"description": ""}
    resume_prompt = createResumePrompt(mock_generator, sample_person, empty_job)
    cover_prompt = createCoverLetterPrompt(mock_generator, sample_person, empty_job)

    assert printPerson(sample_person) in resume_prompt
    assert printPerson(sample_person) in cover_prompt
    assert "Here is a job description:\n" in resume_prompt
    assert "Here is a job description:\n" in cover_prompt
    assert "EmptyField" not in resume_prompt  # Should be filtered out
    assert "EmptyField" not in cover_prompt