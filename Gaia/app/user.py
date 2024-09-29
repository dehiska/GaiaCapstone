from flask_login import UserMixin
from werkzeug.security import check_password_hash

class User(UserMixin):
    def __init__(self, userid, username, email, password, ismod):
        self.userid = userid
        self.username = username
        self.email = email
        self.password = password
        self.ismod = ismod

    def get_id(self):
        return str(self.userid)  # Must return a string for Flask-Login

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)