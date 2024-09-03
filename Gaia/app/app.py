from flask import Flask, render_template, request, flash, redirect, url_for, current_app, session
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from forms import loginForm, registerForm
from models import db, User
from flask_migrate import Migrate
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config['SECRET_KEY'] = 'changeforprod'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Gaia.sqlite3'

from models import db, User
#db = SQLAlchemy(app)

db.init_app(app)

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
default ={}


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

migrate = Migrate(app, db)

@app.route('/testdb')
def testdb():
    dbtest = db.get_or_404(user, 1)
    user = user.query.get(1)
    print(user)
    return f"<h1>('Event: ' + {str(user)})</h1>"

# SPLASH PAGE
@app.route('/')
def index():
    return render_template('index.html')



# LOGIN

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    

    form = loginForm()
    if form.validate_on_submit():
        current_app.logger.info('Form submitted successfully')  # Add this line for debugging

        user = User.query.filter_by(email=form.email.data).first()

        if user and user.password == form.password.data and user.email == form.email.data:
            session['userID'] = user.userid
            session['firstName'] = user.firstname
            current_app.logger.info(user.firstname)  # Add this line for debugging

            if user.ismod:
                login_user(user, remember=True)
                return redirect('/admin')

            login_user(user)
            return redirect(url_for('home')) # Change this to the home page
        
        else:
            flash('Login unsuccessful. Please check your credentials.', 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


class AdminModelView(ModelView):
    def is_accessible(self):
        # Check if user is logged in and is a moderator
        return current_user.is_authenticated and current_user.ismod

    def inaccessible_callback(self, name, **kwargs):
        # If user is not logged in, redirect to login page, else home page
        if not current_user.is_authenticated:
            current_app.logger.info('User is not authenticated')  # Add this line for debugging

        flash('You do not have permission to view the admin page.', 'error')
        return redirect(url_for('login'))
# ADMIN PAGE
admin = Admin(app, name='Admin View', template_mode='bootstrap3')
admin.add_view(AdminModelView(User, db.session))
#admin.add_view(AdminModelView(Event, db.session))   



# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    print('rendering')
    rform = registerForm(request.form)  # Create an instance of the registerForm
    if  request.method == 'POST' and rform.validate_on_submit():
        # Create a User object
        user = User(
            fullName=rform.fullName.data,
            username=rform.username.data,
            email=rform.email.data,
            phone=rform.phone.data,
            password=rform.password.data,
            confirmPassword=rform.password.data
        )
        # Save the user to the database
        db.session.add(user)
        db.session.commit()
        # Redirect to a success page or render a success template
        return redirect(url_for('login'))

    return render_template('regForm.html', form=rform)


# HOME PAGE
#@app.route('/home')
#@login_required
#def home():
#    flair_filter = request.args.get('flair_filter', 'All')

    # Fetch flairs for the dropdown
#    flairs = Flair.query.all()

    # Fetch events based on the selected flair
#    if flair_filter == 'All':
    #     events = Event.query.all()  # Fetch all events if no specific flair is selected
    # else:
    #     # Fetch events based on the selected flair
    #     events = Event.query.join(Event.flairone).filter(Flair.name == flair_filter).all()
    # return render_template('home.html', events=events, flairs=flairs)

# @app.route('/myevents')
# @login_required
# def myevents():
#     print(current_user.userid)
#     user_events = Event.query.filter_by(userID=current_user.userid).all() # Fetch events created by the current user by id
#     return render_template('myevents.html', events=user_events)


#@app.route('/eventview/<int:eventID>', methods=['GET','POST'])
# @login_required
# def eventdetailview(eventID):

#     form = commentForm(request.form)

#     #if comment form is submitted
#     if request.method == 'POST' and form.validate():
#         comment = Comment(
#             userID = current_user.userid,
#             eventID = eventID,
#             message = form.message.data,     
#         )

#         db.session.add(comment)
        
#         try:
#             db.session.commit()
#         except Exception as e:
#             db.session.rollback()
#         flash('There was an issue submitting you comment.')

#         newURL = f'/eventview/{eventID}'
#         return redirect(newURL)
#     #gets entry from primarky key value
#     singleEvent = Event.query.get(eventID)
#     flairName = singleEvent.flairone.name if singleEvent.flairone else "None"  # Retrieve the flairs for the event
#     user_has_rsvped = RSVP.query.filter_by(userID=current_user.userid, eventID=eventID).first() is not None



#     return render_template("eventdetailview.html", singleEvent=singleEvent, flairName=flairName, 
#                 user_has_rsvped=user_has_rsvped, form=form)


# @app.route('/event/<int:event_id>/rsvp', methods=['POST'])
# @login_required
# def rsvp_to_event(event_id):
#     existing_rsvp = RSVP.query.filter_by(userID=current_user.userid, eventID=event_id).first()
    
#     if existing_rsvp:
#         db.session.delete(existing_rsvp)
#         flash('Your RSVP has been removed.', 'info')
#     else:
#         new_rsvp = RSVP(userID=current_user.userid, eventID=event_id)
#         db.session.add(new_rsvp)
#         flash('Your RSVP has been recorded!', 'success')

#     try:
#         db.session.commit()
#     except Exception as e:
#         db.session.rollback()
#         flash('There was an issue updating your RSVP.', 'danger')
    
#     return redirect(url_for('eventdetailview', eventID=event_id))


#@app.route('/create-event', methods=['GET', 'POST'])
#@login_required
# def create_event():
#     form = EventForm(request.form)

#     form.flair.choices = [(0, 'None')] + [(flair.flairID, flair.name) for flair in Flair.query.all()]
#     if request.method == 'POST':
#         print("Form submitted")  # Debug statement
#         if form.validate_on_submit():
#             print("Form validated successfully")  # Debug statement

#             # Temporary user ID for now, replace with actual user ID when login is implemented
#             temp_user_id = current_user.userid

#             try:
#                 # Create a new event instance
#                 new_event = Event(
#                     userID=temp_user_id,
#                     title=form.title.data,
#                     description=form.description.data,
#                     eventTime=form.eventTime.data,
#                     location=form.location.data,
#                     flairone_id=form.flair.data if form.flair.data else None
#                 )

#                 # Add the new event to the database
#                 db.session.add(new_event)
#                 db.session.flush()  # Flush to ensure new_event gets an ID

#                 # Commit changes to the database
#                 db.session.commit()
#                 print('Event created successfully!')  # Debug statement
#                 flash('Event created successfully!', 'success')
#             except Exception as e:
#                 # Handle errors
#                 print(f"An error occurred: {e}")  # Debug statement
#                 db.session.rollback()
#                 flash('Error creating event.', 'error')
#             return redirect(url_for('home'))
#         else:
#             print("Form not validated.")  # Debug statement
#             print(f"Form Errors: {form.errors}")  # Log form errors to help diagnose validation failures
#     else:
#         print("Form not submitted via POST")  # Debug statement

    #return render_template('createEvent.html', form=form, flair=form.flair.choices)

if __name__ == '__main__':
    app.run(debug=True)