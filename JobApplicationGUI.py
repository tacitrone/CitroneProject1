from PyQt5.QtWidgets import *
from Functions import *

# Define the database file
DB_FILE = "jobs.db"

# Main window for the GUI
class JobInfoApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Job Listings")
        self.setGeometry(100, 100, 1000, 600)

        self.jobs_data = self.fetch_jobs_data()  # Fetch jobs from the database
        self.init_ui()

    # Initialize the UI
    def init_ui(self):
        layout = QHBoxLayout()
        LeftSide = QVBoxLayout()
        RightSide = QVBoxLayout()

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

        #Add a submit button:
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.on_submit)  # Connect to the method that handles the button click
        RightSide.addWidget(submit_button)




        #add Left Side to layout
        layout.addLayout(LeftSide)
        layout.addLayout(RightSide)


        # Set the layout for the central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def on_submit(self):
        # Check if all fields are filled
        if not all([
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
            self.NameInput.text(),
            age,
            self.SchoolInput.text(),
            gpa,
            self.ExperienceInput.text(),
            self.skillInput.text(),
            self.projectInput.text(),
            self.emailInput.text(),
            self.phoneInput,
            self.linkedinInput.text(),
            self.addressInput.text(),
            self.classesInput.text()
        )

        create_person_table()
        insert_person_into_db(person)

        # Clear the form after submission
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


