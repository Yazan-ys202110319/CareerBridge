from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()  # Load the environment variables from the .env file

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL) # Load the database to the engine.


def load_jobs_form_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from jobs"))
        jobs = []
        for row in result.all(): # jobs is a list
            jobs.append(row._asdict())
        return jobs