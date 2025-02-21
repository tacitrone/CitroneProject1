import google.generativeai as genai
import json
import sqlite3

# Define the database file
DB_FILE = "jobs.db"



# SQL statement to create the jobs table if it does not exist
CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS jobs (
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


# Function to retrieve the API key from a JSON configuration file
def get_api_key(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data.get("api_key")


# Main function to execute the script
def main():
    # Initialize the AI API with the retrieved API key
    genai.configure(api_key=get_api_key("config.json"))
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Gather user information and parse job data
    myPerson = getUserInfo()
    jobData = parseJSON()
    jobData2 = parse_alternate_json()

    if not jobData:  # Ensure job data is available
        print("Error: No job data found.")
        return
    if not jobData2:
        print("Error: No job data found in JobData2")
        return

    # Create the database and insert parsed job data
    create_database()
    insert_jobs(jobData, sqlite3.connect(DB_FILE))
    insert_jobs(jobData2, sqlite3.connect(DB_FILE))

    # Generate a resume using the AI model
    firstjob = jobData[0]  # Use the first job entry
    response = model.generate_content(
        "Give me a sample resume in markdown format designed for my skills "
        "and the job description I provided.\n"
        f"Here is a description of myself:\n{printPerson(myPerson)}"
        f"\nHere is a job description:\n{firstjob['description']}"
    )

    # Save the generated resume to a file
    print("Resume has been generated successfully. See the file resume.md for the generated resume.")
    with open("resume.md", "w") as file:
        file.write(response.text)


# Class to store user information
class Person:
    def __init__(self, name, age, school, gpa, experience, skills, projects, email, phone, linkedIn, address):
        self.name = name
        self.age = age
        self.school = school
        self.gpa = gpa
        self.experience = experience
        self.skills = skills
        self.projects = projects
        self.email = email
        self.phone = phone
        self.linkedIn = linkedIn
        self.address = address


# Function to guide the user to input necessary information
def getUserInfo():
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    school = input("Enter your school: ")
    gpa = float(input("Enter your GPA: "))
    experience = input("Enter your job experience: ")
    skills = input("Enter your skills: ")
    project = input("Enter any projects you have completed: ")
    email = input("Enter your email: ")
    phone = input("Enter your phone number: ")
    linkedIn = input("Enter your LinkedIn profile link: ")
    address = input("Enter your address: ")
    return Person(name, age, school, gpa, experience, skills, project, email, phone, linkedIn, address)


# Function to parse job data from a JSON file
def parseJSON(filename="fixed_rapidResults.json"):
    with open(filename, "r", encoding="utf-8") as file:
        try:
            data = [json.loads(line) for line in file]
            return data
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return []  # Return an empty list if an error occurs


# Function to parse an alternate job data JSON file
def parse_alternate_json(file_path="rapid_jobs2.json"):
    with open(file_path, "r", encoding="utf-8") as file:
        try:
            data = []
            for line in file:
                parsed_line = json.loads(line)
                if isinstance(parsed_line, list):
                    data.extend(parsed_line)
            return data
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return []


# Function to format person details for output
def printPerson(person):
    return (f"Name: {person.name}\n"
            f"Age: {person.age}\n"
            f"School: {person.school}\n"
            f"GPA: {person.gpa}\n"
            f"Experience: {person.experience}\n"
            f"Skills: {person.skills}\n"
            f"Projects: {person.projects}\n"
            f"Email: {person.email}\n"
            f"Phone: {person.phone}\n"
            f"LinkedIn: {person.linkedIn}\n"
            f"Address: {person.address}\n")


# Function to create the database if it does not exist
def create_database():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(CREATE_TABLE_QUERY)
        conn.commit()


# Function to safely convert a value to float
def safe_float(value):
    try:
        return float(value) if value not in [None, ''] else 0.0
    except ValueError:
        return 0.0


# Function to insert job data into the database
def insert_jobs(data, conn):
    cursor = conn.cursor()
    INSERT_QUERY = """
    INSERT OR IGNORE INTO jobs (id, site, job_url, job_url_direct, title, company, location, job_type, date_posted, salary_source,
    interval, min_amount, max_amount, currency, is_remote, job_level, job_function, company_industry, listing_type, emails, description,
    company_url, company_url_direct, company_addresses, company_num_employees, company_revenue, company_description, logo_photo_url,
    banner_photo_url, ceo_name, ceo_photo_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    for job in data:
        min_amount = safe_float(job.get("min_amount"))
        max_amount = safe_float(job.get("max_amount"))
        cursor.execute(INSERT_QUERY,
                       (job.get("id"), job.get("site"), job.get("job_url"), job.get("job_url_direct"), job.get("title"),
                        job.get("company"), job.get("location"), job.get("job_type"), job.get("date_posted"),
                        job.get("salary_source"), job.get("interval"),
                        min_amount, max_amount, job.get("currency"), job.get("is_remote"), job.get("job_level"),
                        job.get("job_function"),
                        job.get("company_industry"), job.get("listing_type"), job.get("emails"), job.get("description"),
                        job.get("company_url"),
                        job.get("company_url_direct"), job.get("company_addresses"), job.get("company_num_employees"),
                        job.get("company_revenue"),
                        job.get("company_description"), job.get("logo_photo_url"), job.get("banner_photo_url"),
                        job.get("ceo_name"), job.get("ceo_photo_url")))
    conn.commit()


if __name__ == "__main__":
    main()
