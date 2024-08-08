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
            text(f'SELECT * FROM jobs WHERE id = {id}'),
        )
        rows = result.all()
        if len(rows) == 0:
            return None
        else:
            return rows[0].__asdict()