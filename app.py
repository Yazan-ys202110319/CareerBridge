from flask import Flask, render_template, jsonify
from database import load_jobs_form_db

app = Flask(__name__)

@app.route('/')
def home():
    jobs = load_jobs_form_db()
    return render_template('home.html', jobs = jobs)

@app.route("/api/jobs")
def list_jobs():
    return jsonify(JOBS)

if __name__ == '__main__':
    app.run(debug = True)