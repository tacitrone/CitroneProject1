# AI-Powered Resume Generator

## Overview
This project allows you to create a professional resume using AI. Simply provide a brief description of yourself, and the program will generate a customized resume based on your input.

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



## Usage

### 1. Run the Program
Run the script using Python:
```bash
python main.py
```

### 2. Input Your Description
When prompted, provide a short description of yourself, such as your:
- Skills
- Work experience
- Education
- Career goals

### 3. View Your Resume
The program will process your input and generate a professional resume based on the information provided. The resume will be displayed in the console and saved as a file (e.g., `resume.txt` or `resume.pdf`, depending on implementation).

## Example Workflow
1. **Setup**: Add your API key to the `config.json` file.
2. **Run the Program**: Use the command `python main.py`.
3. **Provide Input**: Enter a description like:
   ```
   I am a software engineer with 5 years of experience in Python, specializing in AI and machine learning.
   ```
4. **Generated Output**: The program generates a resume based on your input and saves it to a file.

