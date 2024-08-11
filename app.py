from flask import Flask, render_template, jsonify, request
from database import load_jobs_from_db, load_job_from_db, add_application_to_db
import os
from mailjet_rest import Client


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
    data = request.form # get the user information from the job_page, like the name, email...
    job = load_job_from_db(id)
    add_application_to_db(id, data)


    send_confirmation_email(data['email'], data['full_name'], job['title']) # Send confirmation email to the candidate

    return render_template('application_submitted.html', application = data, job = job)

MAILJET_API_KEY = os.getenv('MAILJET_API_KEY')
MAILJET_SECRET_KEY = os.getenv('MAILJET_SECRET_KEY')

def send_confirmation_email(user_email, user_name, job_title):
    data = { # data is a dictionary
        'Messages' : [ # Messages here is a list containe 1 item.
            {

                # First portion of the dictionary 
                "From": {
                    "Email": "yazan77712366@gmail.com",
                    "Name": "CareerBridge"
                },

                 # Second portion of the dictionary 
                "To": [ # Mailjet API expect a list in the To filed
                    {
                        "Email": user_email,
                        "Name": user_name
                    }
                ],

                # Third portion of the dictionary 
                "Subject": f"Application Received for {job_title}",
                "TextPart": f"Dear {user_name},\n\nThank you for applying to the {job_title} position. We have received your application and will review it shortly.\n\nBest regards,\nCareerBridge",
                "HTMLPart": f"<h3>Dear {user_name},</h3><p>Thank you for applying to the <strong>{job_title}</strong> position. We have received your application and will review it shortly.</p><p>Best regards,<br>CareerBridge</p>"   
                
            }
        ]
    }

    result = mailjet.send.create(data = data)
    if result.status_code == 200: # 200 indicates the request was successful.
        print("Email sent successfully.")
    else:
        print(f"Failed to send email: {result.status_code}")



mailjet = Client(auth=(MAILJET_API_KEY, MAILJET_SECRET_KEY), version='v3.1')

if __name__ == '__main__':
    app.run(debug = True)