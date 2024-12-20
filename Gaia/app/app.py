from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from user import User
import os
import json

from recommendations import Recommendations
from forms import loginForm, registerForm
from database import get_user_by_email, insert_user, get_user_by_id, get_user_recommendations, update_user_recommendations


app = Flask(__name__)
app.config['SECRET_KEY'] = 'changeforprod'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_FILE_DIR'] = './flask_session/'
Session(app)

login_manager = LoginManager()
login_manager.init_app(app)

# Load User by ID for flask_login
@login_manager.user_loader
def load_user(userid):
    user_data = get_user_by_id(userid)
    if user_data:
        return User(user_data['userid'], user_data['username'], user_data['email'], user_data['password'], user_data['ismod'])
    return None

# Splash Page / Login Route
@app.route('/', methods=['GET', 'POST'])
def index():
    form = loginForm()  # Initialize your login form

    # Check if the user is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))  # Redirect to homepage if logged in

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user_data = get_user_by_email(email)  # Get user data by email
        if user_data and check_password_hash(user_data['password'], password):
            user = User(user_data['userid'], user_data['username'], user_data['email'], user_data['password'], user_data['ismod'])
            login_user(user)  # Log the user in
            flash('Login successful!', 'success') 
            return redirect(url_for('homepage'))  # Redirect to homepage after login
        else:
            flash('Invalid credentials, please try again.', 'danger')

    return render_template('index.html', form=form)

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = registerForm()
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        firstName = request.form.get('firstName')  # Updated
        lastName = request.form.get('lastName')    # Updated

        # Check if any field is missing
        if not username or not email or not password or not firstName or not lastName:
            flash('Please fill in all fields.', 'danger')
            return redirect(url_for('register'))

        # Check if the email already exists
        if get_user_by_email(email):
            flash('Email is already registered. Please use a different email.', 'danger')
            return redirect(url_for('register'))

        # Hash the password and insert the new user into the database
        hashed_password = generate_password_hash(password)
        insert_user(username, email, hashed_password, firstName, lastName, created_at='2024-09-29')

        flash('Account created successfully. You can now log in.', 'success')
        return redirect(url_for('index'))

    return render_template('regForm.html', form=form)

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')  # Make sure you have a homepage.html file

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    # print("Logging out user...")  # Debug statement
    logout_user()
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


# #Accepting incoming data from lifestyle Survey
# @app.route('/submit_survey', methods=['POST'])
# def submit_survey():
#     data = request.get_json()

#     if data:
#         # Store the survey data in session
#         session['survey_data'] = data
#         app.logger.info(f"Received data: {data}")
#         # Generate recommendations based on the survey data
#         recommend = Recommendations(data)
#         generate_recommendations = recommend.generate_recommendations()

#         # Save recommendations to session for later use in templates
#         session['recommendations'] = generate_recommendations
#         session['chart_url'] = recommend.graph_electricity_usage()

#         return jsonify({"redirect_url": url_for('recommendations')})

#         # return render_template(
#         #     "recommendations.html",
#         #     recommendations = generate_recommendations, 
#         #     chart_url = chart_url
#     else:
#         return jsonify({"error": "No data received"}), 400

#         # Return a success message
#     #     return jsonify({"message": "Survey data received successfully.", "recommendations": generate_recommendations}), 200
#     # else:
#     #     return jsonify({"error": "No data received"}), 400

#########################################################

# @app.route('/')
# def homepage():
#     return render_template('homepage.html')
@app.route('/submit_survey', methods=['POST'])
def submit_survey():
    try:
        # Get survey data from the request
        survey_data = request.get_json()
        if not survey_data:
            return jsonify({"error": "Invalid survey data"}), 400
        
        print("Survey Data Received:", survey_data)

        # Generate recommendations
        recommender = Recommendations(survey_data)
        generated_recommendations = recommender.generate_recommendations()

        # Save recommendations to a JSON file
        recommendations_file = os.path.join(app.config['SESSION_FILE_DIR'], 'recommendations.json')
        with open(recommendations_file, 'w') as f:
            json.dump(generated_recommendations, f)
        print(f"/submit_survey says: Recommendations saved to {recommendations_file} /submit_survey route here")

        # Generate visualizations
        recommender.generate_visualizations()

        return jsonify({"message": "Survey submitted successfully!"}), 200
    except Exception as e:
        print(f"Error in submit_survey: {str(e)}")
        return jsonify({"error": "An error occurred while processing the survey"}), 500


@app.route('/recommendations', methods=['GET'])
def recommendations():
    try:
        
        # Hardcoded path to the JSON file
        file_path = r"C:\Users\NOSfe\Desktop\Capstone\GaiaCapstone\Gaia\app\survey_recommendations.json"

        # Read recommendations from the file
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                survey_data = json.load(f)
################################################## NEW 11-18-24
            recommender = Recommendations(survey_data)

################################################## NEW 11-18-24
        else: #(REVERT TO THIS IF 11-18-24 DOESN'T WORK) 11-17-24
            survey_data = ["No recommendations found."]
            recommender = Recommendations(survey_data)
        generated_recommendations = recommender.generate_recommendations()

################################################## NEW 11-18-24

        # recommender = Recommendations(survey_data)
        # generated_recommendations = recommender.generate_recommendations()

        graphs = {
            "electricity_kwh": "/static/electricity_usage.png",
            "energy_source": "/static/energy_source.png",
            "car_miles": "/static/car_emissions.png",
            "short_flights": "/static/short_flights.png",
            "long_flights": "/static/long_flights.png",
            "diet": "/static/diet_emissions.png",
            "recycles": "/static/waste_emissions.png"
        }

################################################## NEW 11-18-24

        # Generate visualizations
        recommender.generate_visualizations()

        return render_template( 
            'recommendations.html',
            generated_recommendations=generated_recommendations,
            graphs=graphs
        )

        # Render recommendations.html
        # return render_template( (REVERT TO THIS IF 11-18-24 DOESN'T WORK) 11-17-24
        #     'recommendations.html',
        #     generated_recommendations=generated_recommendations,
        #     graphs={}  # Adjust as needed for graphs
        # )
    except Exception as e:
        print(f"Error in recommendations route: {str(e)}")
        return "An error occurred while retrieving recommendations.", 500



if __name__ == '__main__':
    app.run(debug=True)
