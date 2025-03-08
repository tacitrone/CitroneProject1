import pytest


# Dummy implementation to simulate the printPerson functionality.
def printPerson(person):
    # For testing purposes, simply return a string combining name and location.
    return f"{person['name']} from {person['location']}"


# Functions to create the resume and cover letter prompts.
def create_resume_prompt(myPerson, selected_job):
    return (
        "Give me a sample resume in markdown format designed for my skills "
        "and the job description I provided.\n"
        f"Here is a description of myself:\n{printPerson(myPerson)}"
        f"\nHere is a job description:\n{selected_job['description']}"
    )


def create_cover_letter_prompt(myPerson, selected_job):
    return (
        "Give me a sample cover letter in markdown format designed for my skills "
        "and the job description I provided.\n"
        f"Here is a description of myself:\n{printPerson(myPerson)}"
        f"\nHere is a job description:\n{selected_job['description']}"
    )


# Test to ensure the resume prompt contains both user information and job description.
def test_resume_prompt_contains_user_info_and_job_description():
    # Setup dummy data
    myPerson = {"name": "Alice", "location": "Wonderland"}
    selected_job = {"description": "Looking for a software engineer with AI expertise."}

    resume_prompt = create_resume_prompt(myPerson, selected_job)

    expected_user_info = printPerson(myPerson)
    expected_job_description = selected_job["description"]

    # Check that both expected strings are present in the resume prompt.
    assert expected_user_info in resume_prompt, "Resume prompt does not contain user information."
    assert expected_job_description in resume_prompt, "Resume prompt does not contain job description."


# Test to ensure the cover letter prompt contains both user information and job description.
def test_cover_letter_prompt_contains_user_info_and_job_description():
    # Setup dummy data
    myPerson = {"name": "Alice", "location": "Wonderland"}
    selected_job = {"description": "Looking for a software engineer with AI expertise."}

    cover_letter_prompt = create_cover_letter_prompt(myPerson, selected_job)

    expected_user_info = printPerson(myPerson)
    expected_job_description = selected_job["description"]

    # Check that both expected strings are present in the cover letter prompt.
    assert expected_user_info in cover_letter_prompt, "Cover letter prompt does not contain user information."
    assert expected_job_description in cover_letter_prompt, "Cover letter prompt does not contain job description."
