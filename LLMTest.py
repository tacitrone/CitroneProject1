import os
import pytest
import google.generativeai as genai


@pytest.mark.integration
def test_llm_response_ok():
    # Retrieve the API key from the environment (e.g., set via GitHub Secrets)
    api_key = os.getenv("API_KEY")
    if not api_key:
        pytest.skip("API_KEY environment variable not set; skipping integration test")

    # Configure the client with the API key
    genai.configure(api_key=api_key)

    # Initialize the model (using the provided model name)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Define a test prompt to send to the LLM
    prompt = "Hello, world!"

    # Generate content from the model
    response = model.generate_content(prompt)

    # Assert that the response indicates success (assuming the response object has a status_code attribute)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
