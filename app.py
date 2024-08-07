from flask import Flask, render_template, jsonify

app = Flask(__name__)

JOBS = [
    {
        'id' : 1,
        'title' : 'Data Analyst',
        'location' : 'Doha, Qatar',
        'salary' : 'QR 15000'
    },
    {
        'id' : 2,
        'title' : 'Data Scientist',
        'location' : 'San Francisco, USA',
        'salary' : 'QR 20000'
    },
    {
        'id' : 3,
        'title' : 'Frontend Engineer',
        'location' : 'West Bay, Qatar',
    },
    {
        'id' : 4,
        'title' : 'Backend Engineer',
        'location' : 'New York, USA',
        'salary' : 'QR 25000'
    }
]

@app.route('/')
def home():
    return render_template('home.html', jobs = JOBS)

@app.route("/api/jobs")
def list_jobs():
    return jsonify(JOBS)

if __name__ == '__main__':
    app.run(debug = True)