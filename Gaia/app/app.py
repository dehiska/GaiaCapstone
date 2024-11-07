from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from user import User
from forms import loginForm, registerForm
from database import get_user_by_email, insert_user, get_user_by_id  # Ensure these functions exist
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'changeforprod'

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

@app.route('/recommendations')
def recommendations():
    chart_url = generate_electricity_usage_chart()
    return render_template('recommendations.html', chart_url=chart_url)

def generate_electricity_usage_chart():
    # Get user-specific data (this is an example; adjust based on your actual data source)
    user_data = [10, 15, 10, 20, 25]  # Replace this with actual user data

    # Generate plot based on user data
    plt.figure()
    plt.plot(user_data)  # Plot user data
    plt.title('Electricity Usage Over Time')
    plt.xlabel('Time')
    plt.ylabel('Usage (kWh)')

    # Save the plot to the static folder with a unique name based on user ID
    user_id = 123  # Replace with actual user ID or unique identifier
    img_path = os.path.join('static', f'electricity_usage_chart_{user_id}.png')
    plt.savefig(img_path)
    plt.close()

    return url_for('static', filename=f'electricity_usage_chart_{user_id}.png')


@app.route('/electricity_usage', methods=['GET', 'POST'])
def electricity_usage_data():
    if request.method == 'POST':
        user_data = request.form.getlist('usage_data', type=float)
    else:
        user_data = [10, 15, 10, 20, 25]  # Default or test data
    # Generate and save plot as before

    # Call the function to generate and save the plot image with the provided data
    chart_url = generate_electricity_usage_chart()

    return render_template('recommendations.html', chart_url=chart_url)

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    # print("Logging out user...")  # Debug statement
    logout_user()
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


#Accepting incoming data from lifestyle Survey
@app.route('/submit_survey', methods=['POST'])
def submit_survey():
    data = request.get_json()

    if data:
        # Store the survey data in session
        session['survey_data'] = data

        # Generate recommendations based on the survey data
        recommendations = Recommendations(data).generate_recommendations()

        # Save recommendations to session for later use in templates
        session['recommendations'] = recommendations

        # Return a success message
        return jsonify({"message": "Survey data received successfully.", "recommendations": recommendations}), 200
    else:
        return jsonify({"error": "No data received"}), 400
if __name__ == '__main__':
    app.run(debug=True)
