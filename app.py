from flask import Flask, render_template, jsonify, request, url_for, session, redirect, flash
from database import load_jobs_from_db, load_job_from_db, add_application_to_db, add_user_to_db, load_user_from_db
import os
from mailjet_rest import Client
from dotenv import load_dotenv
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('app_secret_key')
app.permanent_session_lifetime = timedelta(minutes = 5)


DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)


# Landing page 
@app.route('/')
def landing_page():
    return render_template('landing_page.html')



@app.route('/about_us', methods = ['GET'])
def about_us():
    return render_template('about_us.html')


@app.route('/contact_us', methods = ['GET'])
def contact_us():
    return render_template('contact_us.html')
    


@app.route('/login', methods = ['POST', 'GET'])
def login():

    if request.method == "POST":
        
        user_email = request.form.get('email')
        user_password = request.form.get('password1')
         

        getInfoFromDb = load_user_from_db(user_email)

        # if the value of getInfoFromDb is -1 that indecate there is no user with this email or password.
        if getInfoFromDb != -1:
            my_tuple = getInfoFromDb[0]  # Access the first (and only) tuple in the list.

            # my_tuple[0] is the stored email.
            stored_hashed_password = my_tuple[1]
            user_type = my_tuple[2]

            if check_password_hash(stored_hashed_password, user_password):
                session.permanent = True
                session['user_email'] = user_email # identify and store the user by his email because it is unique.
                # session is a dictionary and 'user_email' is key and user_email is a value.
                session['user_type'] = user_type # Store the user type.
                flash("Logged in successfully!", category = 'success')

                return redirect(url_for('home'))
            
            if 'user_email' in session:
                return redirect(url_for('home'))
            
            # Check if the user is already logged in redirect him immediately and no need to log in again. and do not need unnecessary processing.
            elif 'user_email' not in session:
                return render_template('login.html')
            
            else:
                # flash a message about wrong email or password
                return render_template('login.html')
        else:
            # flash a message about no user with this email
            return render_template('login.html')

    return render_template('login.html')


@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    if request.method == 'POST':

        user_data = request.form

        user_name = request.form.get('user_name')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(user_name) < 2:
            flash("Your name must be grater than 1 character.", category = 'error')
        elif len(email) < 4:
            flash("Email must be grater than 3 characters.", category = 'error')
        elif len(password1) < 7:
            flash("Passwords must be at least 7 characters.", category = 'error')
        elif password1 != password2:
            flash("Passwords don't match.", category = 'error')
        else:
            hashed_password = generate_password_hash(user_data['password1'], method = 'pbkdf2:sha256')
            user_data = {
                'user_name': user_name,
                'email': email,
                'password1': hashed_password,
                'password2': hashed_password
            }

            flash("Account created successfully!", category = 'success')
            add_user_to_db(user_data)
            return redirect(url_for('home'))


        return redirect(url_for('signup'))
    
    else: # here for the get method
        return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user_email', None) # To delete the user information from the session.
    flash('You have been logged out.', category = 'correct')
    return redirect(url_for('landing_page'))
     


@app.route('/add_job', methods = ['GET'])
def add_job():

    if 'user_email' in session:
        user_email = session['user_email']

        # Load all user info with the same email
        user_info_list = load_user_from_db(user_email)

        if user_info_list != 1:
            for user_info in user_info_list:
                user_type = user_info[2]
                if user_type == 'admin':
                    return render_template('add_job.html')
                
            # No admin found after iterating through all users
            flash('Access denied. Admins only.', category = 'error')
            return redirect(url_for('home'))
        else:
            flash('No user with this email.', category = 'error')
            return redirect(url_for('login'))
            
    else:
        flash('Please log in to access this page.', category = 'error')
        return redirect(url_for('login'))



# home page
@app.route('/home')
def home():
    if 'user_email' in session: # if user still in session.
        # user is logged in
        user_email = session['user_email'] # To get the user
        jobs = load_jobs_from_db()
        return render_template('home.html', jobs = jobs) 
    else:
        # User is not logged in
        flash('Please log in to access this page.', category = 'error')
        return redirect(url_for('login'))


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


 
@app.route('/job/<id>/apply', methods = ['POST'])
def apply_to_job(id): # id is the job id
    data = request.form # get the user information from the job_page, like the name, email...
    job = load_job_from_db(id)
    add_application_to_db(id, data)


    send_confirmation_email(data['email'], data['full_name'], job['title']) # Send confirmation email to the candidate

    return render_template('application_submitted.html', application = data, job = job)



MAILJET_API_KEY = os.getenv('MAILJET_API_KEY')
MAILJET_SECRET_KEY = os.getenv('MAILJET_SECRET_KEY')
# create an instance of the mailjet client to interact with mailjet api
mailjet = Client(auth = (MAILJET_API_KEY, MAILJET_SECRET_KEY), version = 'v3.1')



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



if __name__ == '__main__':
    app.run(debug = True)