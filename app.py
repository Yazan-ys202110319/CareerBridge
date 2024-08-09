from flask import Flask, render_template, jsonify, request
from database import load_jobs_from_db, load_job_from_db, add_application_to_db

app = Flask(__name__)

@app.route('/')
def home():
    jobs = load_jobs_from_db()
    return render_template('home.html', jobs = jobs)


@app.route("/api/jobs")
def list_jobs():
    jobs = load_jobs_from_db()
    return jsonify(jobs)


@app.route('/job/<id>')
def show_job(id):
    job = load_job_from_db(id)
    if not job:
        return "Not Fount", 404
    return render_template('job_page.html', job = job)

 
@app.route('/job/<id>/apply', methods = ['post'])
def apply_to_job(id): # id is the job id
    data = request.form # get the user information from the job_page
    print("Form data:", data)
    job = load_job_from_db(id)
    print(job)
    add_application_to_db(id, data)
    return render_template('application_submitted.html', application = data, job = job)

if __name__ == '__main__':
    app.run(debug = True)