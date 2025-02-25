# AI-Powered Resume Generator

## Updates:
This program now interacts with the user through an GUI using PyQt. The interface allows the user to browse the job listing
database and select certain jobs to see more information on that specific job. It also guides the user through some questions
to gather information about them, and saves that information in order to (in the future) create a tailored resume.

## Prerequisites
Before running the program, you must complete the following setup steps.

### 1. Set Up the `config.json` File
1. Create a file named `config.json` in the same directory as the code.
2. Add the following content to the file, replacing `your_api_key_here` with the API key sent to you via email:
   ```json
   {
       "api_key": "your_api_key_here"
   }
   ```
### 2. Download the dependencies in `requirements.txt`

### 3. Run using `main.py`


## Test Functions:
The JobInfoTest.py tests that when the user selects a job, the correct expanded info is shown.
The UserDataTest.py tests that when the user inputs there data it is correctly inputed into the person database
The FileReaderTest.py tests the parsing of the JSON file.
The DatabaseTest.py tests the creation and insertion of the database.

