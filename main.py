import google.generativeai as genai
import json
import sqlite3

# define job db file
DB_FILE = "jobs.db"


# define the table creation SQL statement
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
# gets API key
def get_api_key(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data.get("api_key")


def main():
    # Initializes AI API
    genai.configure(api_key=get_api_key("config.json"))
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Gets user description and Job description
    #myPerson = getUserInfo()
    jobData = parseJSON()
    #jobData2 = parse_alternate_json()
    if not jobData:  # If jobData is empty, stop execution
        print("Error: No job data found.")
        return
   # if not jobData2:
    #    print("Error: No job data found. in JobData2")
     #   return


    # dummy info:
    myPerson = person("John Doe", 21, "Bridgewater State University", 3.7,
                      "Assistant Manager at Market Basket since 2019", "Java, Python, Communication", "MA Payroll Database Sorter",
                      "JohnDoe@gmail.com", "123-456-7891", "www.linkedin.com/JohnDoe", "123 Unemployed Ave, Bridgewater MA, 12345")

    create_database()
    insert_jobs(jobData,sqlite3.connect(DB_FILE) )
    #insert_jobs(jobData2)

    firstjob = jobData[0]  # Ensure there's at least one job
    response = model.generate_content(
       "Give me a sample resume in markdown format designed for my skills "
       "and the job description I provided.\n"
        f"Here is a description of myself:\n{printPerson(myPerson)}"
        f"\nHere is a job description:\n{firstjob['description']}"
    )
    # prints response
    print("Resume has been generated successfully. See the file resume.md for the generated resume.")

    with (open("resume.md", "w")) as file:
        file.write(response.text)

class person:
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



def getUserInfo(): # guides the user to give necessary information
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    school = input("Enter your school: ")
    gpa = float(input("Enter your GPA: "))
    experience = input("Enter your job experience: ")
    skills = input("Enter your skills: ")
    project = input("Enter any projects you have completed: ")
    email = input("Enter your email: ")
    phone = input("Enter your phone number: ")
    linkedIn = input("Enter your linkedIn link: ")
    address = input("Enter your address: ")
    return person(name, age,school, gpa, experience, skills, project, email, phone, linkedIn, address)


def parseJSON(filename="fixed_rapidResults.json"):
    with open(filename, "r", encoding="utf-8") as file:
        try:
            data = []
            for line in file:
                try:
                    # Parse each line and append to the data list
                    data.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"Error parsing line: {e}")
            return data
        except Exception as e:
            print(f"Error reading the file: {e}")
            return []  # Return an empty list if something goes wrong


def parse_alternate_json(file_path="rapid_jobs2.json"):
    with open(file_path, "r", encoding="utf-8") as file:
        try:
            data = []
            for line in file:
                try:
                    # Parse each line and append to the data list
                    data.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"Error parsing line: {e}")

            transformed_data = []
            for job in data:
                # Ensure 'job' is a dictionary and handle missing fields
                if isinstance(job, dict):
                    transformed_job = {
                        "id": job.get("id", ""),
                        "site": "Unknown",
                        "job_url": job["jobProviders"][0]["url"] if isinstance(job.get("jobProviders"), list) and len(
                            job["jobProviders"]) > 0 else "",
                        "job_url_direct": job["jobProviders"][0]["url"] if isinstance(job.get("jobProviders"),
                                                                                      list) and len(
                            job["jobProviders"]) > 0 else "",
                        "title": job.get("title", ""),
                        "company": job.get("company", ""),
                        "location": job.get("location", ""),
                        "job_type": job.get("employmentType", ""),
                        "date_posted": job.get("datePosted", ""),
                        "salary_source": "Unknown",
                        "interval": "yearly",
                        "min_amount": None,
                        "max_amount": None,
                        "currency": "USD",
                        "is_remote": "False",
                        "job_level": "Unknown",
                        "job_function": "Unknown",
                        "company_industry": "Unknown",
                        "listing_type": "Aggregated",
                        "emails": "",
                        "description": job.get("description", ""),
                        "company_url": "",
                        "company_url_direct": "",
                        "company_addresses": "",
                        "company_num_employees": "",
                        "company_revenue": "",
                        "company_description": "",
                        "logo_photo_url": job.get("image", ""),
                        "banner_photo_url": "",
                        "ceo_name": "",
                        "ceo_photo_url": ""
                    }
                    transformed_data.append(transformed_job)

            return transformed_data
        except Exception as e:
            print(f"Error reading the file: {e}")
            return []

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

#CREATE DATABASE
def create_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(CREATE_TABLE_QUERY)
    conn.commit()
    conn.close()


def safe_float(value):
    try:
        # Try to convert the value to a float
        return float(value) if value not in [None, ''] else 0.0
    except ValueError:
        # If conversion fails, return 0.0
        return 0.0

def insert_jobs(data, conn):
    cursor = conn.cursor()

    INSERT_QUERY = """
    INSERT OR IGNORE INTO jobs (
        id, site, job_url, job_url_direct, title, company, location, job_type, date_posted, salary_source,
        interval, min_amount, max_amount, currency, is_remote, job_level, job_function, company_industry,
        listing_type, emails, description, company_url, company_url_direct, company_addresses, company_num_employees,
        company_revenue, company_description, logo_photo_url, banner_photo_url, ceo_name, ceo_photo_url
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """

    for job in data:
        # Safely convert min_amount and max_amount
        min_amount = safe_float(job.get("min_amount"))
        max_amount = safe_float(job.get("max_amount"))

        cursor.execute(INSERT_QUERY, (
            job.get("id"), job.get("site"), job.get("job_url"), job.get("job_url_direct"),
            job.get("title"), job.get("company"), job.get("location"), job.get("job_type"),
            job.get("date_posted"), job.get("salary_source"), job.get("interval"),
            min_amount, max_amount, job.get("currency"),
            job.get("is_remote"), job.get("job_level"), job.get("job_function"),
            job.get("company_industry"), job.get("listing_type"), job.get("emails"),
            job.get("description"), job.get("company_url"), job.get("company_url_direct"),
            job.get("company_addresses"), job.get("company_num_employees"),
            job.get("company_revenue"), job.get("company_description"), job.get("logo_photo_url"),
            job.get("banner_photo_url"), job.get("ceo_name"), job.get("ceo_photo_url")
        ))

    conn.commit()  # Ensure changes are saved



if __name__ == "__main__":
    main()
