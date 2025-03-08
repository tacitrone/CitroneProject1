import pytest
import os
from src.Functions import parseJSON


@pytest.fixture
def setup_test_file():
    # Create a test file with known data
    test_filename = "test_fixed_rapidResults.json"
    test_data = [
        '{"name": "item1", "value": 10}',
        '{"name": "item2", "value": 20}',
        '{"name": "item3", "value": 30}',
        '{"name": "item4", "value": 40}',
    ]

    with open(test_filename, "w", encoding="utf-8") as file:
        for line in test_data:
            file.write(line + "\n")

    # Return the test filename for use in the tests
    yield test_filename

    # Clean up the test file after tests
    os.remove(test_filename)


def test_parseJSON_valid_data(setup_test_file):
    # Get the test filename from the fixture
    test_filename = setup_test_file

    # Call the function to test
    result = parseJSON(test_filename)

    # Assert that the number of items returned is correct
    assert len(result) == 4, "Number of items should be 4"

    # Assert the first item matches expected data
    assert result[0]["name"] == "item1", "First item should be 'item1'"

    # Assert the last item matches expected data
    assert result[-1]["name"] == "item4", "Last item should be 'item4'"

    # Assert the second item has the correct value
    assert result[1]["value"] == 20, "Second item should have value 20"

    # Check if there's a middle item with expected value
    assert result[2]["value"] == 30, "Middle item should have value 30"
