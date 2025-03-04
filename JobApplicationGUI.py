from PyQt5.QtWidgets import *
from Functions import *
from google.generativeai import *

# Define the database file
DB_FILE = "jobs.db"



# Main window for the GUI
class JobInfoApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Job Listings")
        self.setGeometry(100, 100, 1000, 1000)

        self.jobs_data = self.fetch_jobs_data()  # Fetch jobs from the database
        self.init_ui()

    # Initialize the UI
    def init_ui(self):
        layout = QVBoxLayout()
        main_layout = QHBoxLayout()
        LeftSide = QVBoxLayout()
        RightSide = QVBoxLayout()
        Bottom = QHBoxLayout()
        BottomLeft = QVBoxLayout()
        BottomRight = QVBoxLayout()

        # Create a list widget to show job titles
        self.job_list_widget = QListWidget()
        self.job_list_widget.addItems([job['title'] for job in self.jobs_data])  # Populate the list with job titles
        self.job_list_widget.clicked.connect(self.show_job_details)  # Connect the click event

        # Create a text area to display job details
        self.job_details_text = QTextEdit()
        self.job_details_text.setReadOnly(True)

        # Create a refresh button
        self.refresh_button = QPushButton("Refresh Job Data")
        self.refresh_button.clicked.connect(self.refresh_job_data)  # Connect refresh event

        #Create a Form
        self.ProfileName = QLabel("Profile")
        self.ProfileInput = QLineEdit()
        self.NameLabel = QLabel("Name")
        self.NameInput = QLineEdit()
        self.AgeLabel = QLabel("Age")
        self.AgeInput = QLineEdit()
        self.SchoolLabel = QLabel("School")
        self.SchoolInput = QLineEdit()
        self.GPALabel = QLabel("GPA")
        self.GPAInput = QLineEdit()
        self.ExperienceLabel = QLabel("Experience")
        self.ExperienceInput = QLineEdit()
        self.skillLabel = QLabel("Skills")
        self.skillInput = QLineEdit()
        self.projectLabel = QLabel("Projects")
        self.projectInput = QLineEdit()
        self.emailLabel = QLabel("Email")
        self.emailInput = QLineEdit()
        self.phoneLabel = QLabel("Phone Number")
        self.phoneInput = QLineEdit()
        self.linkedinLabel = QLabel("LinkedIn Link")
        self.linkedinInput = QLineEdit()
        self.addressLabel = QLabel("Address")
        self.addressInput = QLineEdit()
        self.classesLabel = QLabel("Any Relevant Classes")
        self.classesInput = QLineEdit()



        # Add the widgets to the Left Side
        LeftSide.addWidget(QLabel("Available Job Listings"))
        LeftSide.addWidget(self.job_list_widget)
        LeftSide.addWidget(self.refresh_button)
        LeftSide.addWidget(QLabel("Job Details"))
        LeftSide.addWidget(self.job_details_text)

        #Add the widgets to the Right Side:
        RightSide.addWidget(QLabel("Please fill out this form to add your information to the resume database."))
        RightSide.addWidget(self.ProfileName)
        RightSide.addWidget(self.ProfileInput)
        RightSide.addWidget(self.NameLabel)
        RightSide.addWidget(self.NameInput)
        RightSide.addWidget(self.AgeLabel)
        RightSide.addWidget(self.AgeInput)
        RightSide.addWidget(self.SchoolLabel)
        RightSide.addWidget(self.SchoolInput)
        RightSide.addWidget(self.GPALabel)
        RightSide.addWidget(self.GPAInput)
        RightSide.addWidget(self.ExperienceLabel)
        RightSide.addWidget(self.ExperienceInput)
        RightSide.addWidget(self.skillLabel)
        RightSide.addWidget(self.skillInput)
        RightSide.addWidget(self.projectLabel)
        RightSide.addWidget(self.projectInput)
        RightSide.addWidget(self.emailLabel)
        RightSide.addWidget(self.emailInput)
        RightSide.addWidget(self.phoneLabel)
        RightSide.addWidget(self.phoneInput)
        RightSide.addWidget(self.linkedinLabel)
        RightSide.addWidget(self.linkedinInput)
        RightSide.addWidget(self.addressLabel)
        RightSide.addWidget(self.addressInput)
        RightSide.addWidget(self.classesLabel)
        RightSide.addWidget(self.classesInput)

        # Profile Selection Dropdown
        self.profile_dropdown = QComboBox()
        self.profile_dropdown.addItems(self.fetch_profiles())  # Fetch and populate profiles

        # Create Resume Button
        self.create_resume_button = QPushButton("Create Resume")
        self.create_resume_button.clicked.connect(self.create_resume)


        #Add a submit button:
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.on_submit)  # Connect to the method that handles the button click
        RightSide.addWidget(submit_button)


        #Bottom Area for Profile Selection and Create Resume Button:
        BottomRight.addWidget(self.create_resume_button)
        BottomLeft.addWidget(self.profile_dropdown)


        #add Left Side to layout
        main_layout.addLayout(LeftSide)
        main_layout.addLayout(RightSide)
        layout.addLayout(main_layout)


        # Set the layout for the central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        #Add bottom to layout:
        Bottom.addLayout(BottomLeft)
        Bottom.addLayout(BottomRight)
        layout.addLayout(Bottom)

    def create_resume(self):
        selected_profile = self.profile_dropdown.currentText()  # Get selected profile name
        selected_index = self.job_list_widget.currentRow()  # Get selected job index

        if not selected_profile:
            QMessageBox.warning(self, "No Profile Selected", "Please select a profile before generating a resume.")
            return

        if selected_index < 0:
            QMessageBox.warning(self, "No Job Selected", "Please select a job before generating a resume.")
            return

        # Fetch the selected job details
        selected_job = self.jobs_data[selected_index]

        # Fetch the full profile details based on the selected profile name
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM person WHERE profile = ?", (selected_profile,))
        person_data = cursor.fetchone()
        conn.close()

        if not person_data:
            QMessageBox.warning(self, "Profile Not Found", "The selected profile could not be found in the database.")
            return

        # Create a formatted string of person details
        myPerson = {
            "Profile": person_data[1],
            "Name": person_data[2],
            "Age": person_data[3],
            "School": person_data[4],
            "GPA": person_data[5],
            "Experience": person_data[6],
            "Skills": person_data[7],
            "Projects": person_data[8],
            "Email": person_data[9],
            "Phone": person_data[10],
            "LinkedIn": person_data[11],
            "Address": person_data[12],
            "Classes": person_data[13]
        }

        # Generate the resume using the AI model
        prompt = (
            "Give me a sample resume in markdown format designed for my skills "
            "and the job description I provided.\n"
            f"Here is a description of myself:\n{printPerson(myPerson)}"
            f"\nHere is a job description:\n{selected_job['description']}"
        )
        prompt2 = ("Give me a sample cover letter in markdown format designed for my skills "
            "and the job description I provided.\n"
            f"Here is a description of myself:\n{printPerson(myPerson)}"
            f"\nHere is a job description:\n{selected_job['description']}")

        genai.configure(api_key=get_api_key("config.json"))
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        response2 = model.generate_content(prompt2)

        # Display the generated resume (assuming Markdown output)
        resume_text = response.text
        cover_letter = response2.text
        self.job_details_text.setPlainText(resume_text)  # Show in job details text box

        # Optionally, save the resume to a file
        with open("resume.md", "w") as file:
            file.write(resume_text)

        with open("coverletter.md", "w") as file:
            file.write(cover_letter)

        QMessageBox.information(self, "Resume and Cover Letter Generated",
                                "The resume has been generated and saved as 'generated_resume.pdf', the Cover Letter has been saved as "
                                "generated_cover_letter.pdf")

        convert_md_to_pdf("resume.md", "generated_resume.pdf")
        convert_md_to_pdf("coverletter.md", "generated_coverletter.pdf")

    def on_submit(self):
        # Check if all fields are filled
        if not all([
            self.ProfileInput.text(),
            self.NameInput.text(),
            self.AgeInput.text(),
            self.SchoolInput.text(),
            self.GPAInput.text(),
            self.ExperienceInput.text(),
            self.skillInput.text(),
            self.projectInput.text(),
            self.emailInput.text(),
            self.phoneInput.text(),
            self.linkedinInput.text(),
            self.addressInput.text(),
            self.classesInput.text()
        ]):
            # Show a message box if any field is empty
            QMessageBox.warning(self, "Form Incomplete", "Please fill in all the fields.")
            return  # Stop further execution if the form is incomplete

        # Validate the 'Age' field to ensure it's an integer
        try:
            age = int(self.AgeInput.text())
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid age (integer).")
            return

        # Validate the 'GPA' field to ensure it's a float
        try:
            gpa = float(self.GPAInput.text())
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid GPA (float).")
            return

        # Proceed with creating the person object if validation is successful
        person = Person(
            self.ProfileInput.text(),
            self.NameInput.text(),
            age,
            self.SchoolInput.text(),
            gpa,
            self.ExperienceInput.text(),
            self.skillInput.text(),
            self.projectInput.text(),
            self.emailInput.text(),
            self.phoneInput.text(),
            self.linkedinInput.text(),
            self.addressInput.text(),
            self.classesInput.text()
        )

        create_person_table()
        insert_person_into_db(person)

        # Refresh the profile dropdown by fetching updated profiles
        self.profile_dropdown.clear()  # Clear the current dropdown
        self.profile_dropdown.addItems(self.fetch_profiles())  # Add the new profiles

        # Clear the form after submission
        self.ProfileInput.clear()
        self.NameInput.clear()
        self.AgeInput.clear()
        self.SchoolInput.clear()
        self.GPAInput.clear()
        self.ExperienceInput.clear()
        self.skillInput.clear()
        self.projectInput.clear()
        self.emailInput.clear()
        self.phoneInput.clear()
        self.linkedinInput.clear()
        self.addressInput.clear()
        self.classesInput.clear()

    # Fetch jobs data from the database
    def fetch_jobs_data(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM jobs")
        jobs = cursor.fetchall()
        conn.close()

        # Map the job data to a dictionary for easy access
        job_data = []
        for job in jobs:
            job_data.append({
                'id': job[0],
                'title': job[4],
                'company': job[5],
                'location': job[6],
                'job_type': job[7],
                'date_posted': job[8],
                'salary_source': job[9],
                'description': job[20]
            })

        return job_data

    # Show the details of the selected job
    def show_job_details(self):
        selected_index = self.job_list_widget.currentRow()
        selected_job = self.jobs_data[selected_index]

        job_details = (
            f"Title: {selected_job['title']}\n"
            f"Company: {selected_job['company']}\n"
            f"Location: {selected_job['location']}\n"
            f"Job Type: {selected_job['job_type']}\n"
            f"Date Posted: {selected_job['date_posted']}\n"
            f"Salary Source: {selected_job['salary_source']}\n"
            f"\nDescription:\n{selected_job['description']}"
        )

        self.job_details_text.setText(job_details)

    # Function to refresh the job data by reparsing the JSON and updating the database
    def refresh_job_data(self):
        print("Refreshing job data...")

        # Re-parse the JSON files and insert new job data into the database
        jobData = parseJSON()  # Re-parse the main job data
        jobData2 = parse_alternate_json()  # Re-parse the alternate job data

        if not jobData and not jobData2:
            print("Error: No job data found.")
            return

        # Insert job data into the database
        insert_jobs(jobData, sqlite3.connect(DB_FILE))
        insert_jobs(jobData2, sqlite3.connect(DB_FILE))

        # Re-fetch the updated job data from the database
        self.jobs_data = fetch_jobs_data()

        # Update the list widget with the new job data
        self.job_list_widget.clear()
        self.job_list_widget.addItems([job['title'] for job in self.jobs_data])

    def fetch_profiles(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT profile FROM person")  # Fetch only profile names
            profiles = [row[0] for row in cursor.fetchall()]
        except sqlite3.OperationalError:
            # If the person table does not exist, return an empty list
            profiles = []
        finally:
            conn.close()

        return profiles if profiles else ["No Profiles Available"]  # Avoid empty dropdown

