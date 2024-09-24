from app import app, db, User  # Make sure to import your app instance

# Create a new user
newuser = User(username="dsoul", email="denissoulima@gmail.com", phone="2032032003", password="123123", fullName="Denis Soulima")

# Use the application context to interact with the database
with app.app_context():
    db.session.add(newuser)
    db.session.commit()

print(newuser)
