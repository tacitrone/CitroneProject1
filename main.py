import google.generativeai as genai
import json

#gets API key
def get_api_key(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data.get("api_key")
# Initializes AI API
genai.configure(api_key=get_api_key("config.json"))
model = genai.GenerativeModel("gemini-1.5-flash")

#Gets user description and Job description
Description = input("Enter a discription of yourself, for example (Age, schooling experience, job experience, skills etc.): ")
JobDescription = "SYNERGISTICIT is aware that the Job Market is Challenging due to almost 600,000 Tech Layoffs within the past 2 years due to which The Job market is flooded with thousands of laid off Techies who are competing with existing Jobseekers. For entry level Job seekers to get client interviews and jobs they need to differentiate themselves by ensuring they have exceptional skills and technologies to be noticed by clients.\n\nSince 2010 we have helped Jobseekers differentiate themselves by providing the clients with candidates who have the requisite skills and experience to outperform at interviews and clients. Here at SynergisticIT We just don't focus on getting you a Job we make careers.\n\nAll Positions are open for all visas and US citizens\n\nWe are matchmakers we provide clients with candidates who can perform from day 1 of starting work. In this economy no client wants or has the resources to take an entry level person and spend resources on upgrading their skills and on top of that pay the jobseeker. That's the specific reason there are so many techies both experience and freshers who are unemployed.\n\nClients have now the option to hire remote workers from anywhere so for a Jobseeker its important to introspect and see how they can become better and have the skills and technologies to meet client requirements.\n\nWe at Synergisticit understand the problem of the mismatch between employer's requirements and Employee skills and that's why since 2010 we have helped thousands of candidates get jobs at technology clients like apple, google, Paypal, western union, Client, visa, walmart labs etc to name a few.\n\nWho Should Apply Recent Computer science/Engineering /Mathematics/Statistics or Science Graduates looking to make their careers in IT Industry\n\nWe welcome candidates with all visas and citizens to apply.\n\nIf you get emails from our skill enhancement team please ask them to take you off their distribution list and make you unavailable as they share the same database with the client servicing team.\n\nplease check the below links to see success outcomes of our candidates"


#generates response
response = model.generate_content("Give me a sample resume in markdown format that will be designed "
                                  "for my skills and the job description I provided. Here is a discription of myself:" + Description
                                  + "here is a job description: " + JobDescription )
#prints response
print("Resume has been generated successfully. See the file resume.md for the generated resume.")

with (open ("resume.md", "w")) as file:
    file.write(response.text)