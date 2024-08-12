from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()  # Load the environment variables from the .env file.

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL) # Load the database to the engine.


def load_jobs_from_db():
    with engine.connect() as conn: # with ensures that the connection is automatically closed when the block is exited.
        result = conn.execute(text("select * from jobs"))
        jobs = []
        for row in result.all(): # jobs is a list
            jobs.append(row._asdict())
        return jobs
    
def load_user_from_db():
    with engine.connect() as conn:
        result = conn.execute(text('SELECT * FROM users'))
        jobs = []
        for row in result.all():
            jobs.append(row._asdict())
        return jobs

def load_job_from_db(id):
    with engine.connect() as conn:
        result = conn.execute(
            text(f'SELECT * FROM jobs WHERE id = {id}')
        )
        rows = result.all()
        if len(rows) == 0:
            return None
        else:
           return rows[0]._asdict()

def load_user_from_db(user_email):
      with engine.connect() as conn:

            query = text(f'SELECT email, password1 FROM users where email = :user_email')

            result = conn.execute(
                query, 
                {
                    'user_email' : user_email,
                }
            )

            temp = result.fetchall()

            if len(temp) == 0:
                return -1
            else:
                return temp

        #   rows = result.all()
        #   if len(rows) == 0:
        #       return -1
        #   else:
        #       return rows[0]._asdict()


def add_user_to_db(user_data):
    user_type = 'user'
    if user_data['email'] == "yazan77712366@gmail.com":
        user_type = 'admin'
    with engine.connect() as conn:
        query = text(f"INSERT INTO users(user_name, email, user_type ,password1, password2) VALUES (:user_name, :email, :user_type ,:password1, :password2)")

        conn.execute(
            query, 
            {
                "user_name" : user_data['user_name'],
                "email": user_data['email'],
                "user_type": user_type,
                "password1": user_data['password1'],
                "password2": user_data['password2'],
            },
        )

        conn.commit()



def add_application_to_db(job_id, data): # data here is the application, and job means which job type the user want to apply.
    with engine.connect() as conn:
        query = text( # query create SQL query string for sqlalchemy.
            # The place holders (:job_id, :full_name) to avoid SQL injuction.
            f"INSERT INTO applications(job_id, full_name, email, linkedin_url, education, work_experience, resume) VALUES (:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume)"
        )

        conn.execute( # execute() runs the SQL query.
            query,
            {
                "job_id": job_id, # because there is only 1 value in the job_id which is the job id there is no need to specify the index like the application.
                "full_name": data["full_name"], # This is the way on how to access the data like a normal dictionary. see below the details.
                "email": data["email"],
                "linkedin_url": data["linkedin_url"],
                "education": data["education"],
                "work_experience": data["work_experience"],
                "resume": data["resume"],
            },
        )
        conn.commit()
        
# You will recive the data from the form using the flask object which is (request) from the form that is sumbmitted by the user, the request return from the web browser "ImmutableMultiDict" which is a specific type of dictionary provided by Flask.

# The HTML :
#    <form method="post">
    #   <input type="text" name="full_name" value="John Doe">
    #   <input type="email" name="email" value="john@example.com">
    #   <input type="text" name="linkedin_url" value="http://linkedin.com/johndoe">
    #   <input type="text" name="education" value="Computer Science">
    #   <input type="text" name="work_experience" value="Software Engineer at XYZ">
    #   <input type="text" name="resume" value="Link to resume">
    #   <input type="submit" value="Apply">
#   </form>

# When the form is submitted, request.form in the app.py it will contain:
#     ImmutableMultiDict([
#     ('full_name', 'John Doe'),
#     ('email', 'john@example.com'),
#     ('linkedin_url', 'http://linkedin.com/johndoe'),
#     ('education', 'Computer Science'),
#     ('work_experience', 'Software Engineer at XYZ'),
#     ('resume', 'Link to resume')
#   ])

# Even though it's immutable, we can still access its data like a regular dictionary:

    # full_name = data['full_name']
    # email = data['email']