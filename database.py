from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()  # Load the environment variables from the .env file

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL) # Load the database to the engine.


def load_jobs_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from jobs"))
        jobs = []
        for row in result.all(): # jobs is a list
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
        
def add_application_to_db(job_id, data):

    with engine.connect() as conn:
        query = text("""INSERT INTO applications (job_id, full_name, email, linkedin_url, education, work_experience, resume) VALUES (1, 'Test Name', 'test@example.com', 'http://linkedin.com/test', 'Test Education', 'Test Experience', 'N/A')""")
    # :job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume)
        result = conn.execute(query, {
            'job_id': job_id,
            'full_name': data['full_name'],
            'email': data['email'],
            'linkedin_url': data['linkedin_url'],
            'education': data['education'],
            'work_experience': data['work_experience'],
            'resume': data['resume']
        })
        
        print(f"Inserted {result.rowcount} row(s) into the database.")

        
        # job_id = job_id, full_name = data['full_name'],
        #              email = data['email'],
        #              linkedin_url = data['linkedin_url'],
        #              education = data['education'],
        #              work_experience = data['work_experience'],
        #              resume = data['resume']


        # 'job_id' : job_id, 'full_name' : data['full_name'],
        #              'email' : data['email'],
        #              'linkedin_url' : data['linkedin_url'],
        #              'education' : data['education'],
        #              'work_experience' : data['work_experience'],
        #              'resume' : data['resume']})