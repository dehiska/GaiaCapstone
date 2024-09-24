
from datetime import datetime
from flask_login import UserMixin
import pytz
import json
from sqlalchemy import UniqueConstraint

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



# > flask shell
# >>>from app import db
# >>>db.create_all()

# HOW TO INSERT DATA
# >>> from app import db, Event, User
# >>> newuser = User(username='john_doe', email='john@example.com', password='password123', firstname='John', lastname='Doe', bio='Some bio')
# >>> db.session.add(newuser)
# >>> db.session.commit()
# >>> db.session.close()

# HOW TO UPDATE DATABASE FILE AFTER CHANGING SCHEMA
# To create a new migration:
# flask db migrate

# To apply the migration and update the database schema:
# flask db upgrade

# To downgrade the database schema (optional, if needed):
# flask db downgrade



class User(db.Model, UserMixin):
    """Model for user accounts."""
    __tablename__ = 'user'

    userid = db.Column(db.Integer,
                   primary_key=True)
    username = db.Column(db.String(40),
                         nullable=False,
                         unique=True)
    email = db.Column(db.String(40),
                      unique=True,
                      nullable=False)
    password = db.Column(db.String(200),
                         unique=False,
                         nullable=False)
    fullName = db.Column(db.String(40),
                         nullable=False)
    ismod = db.Column(db.Boolean,
                           default=False)
    
    def get_id(self):
            return (self.userid)
        
    #ADD THESE LATER
    #posts = db.relationship('Event', backref='author', lazy='dynamic')
    
    #NOT NEEDED: if you need all the comments of the user, user query the Comment table with userID
    #comments = db.relationship('Comment', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class EcoScore(db.Model, UserMixin):
        """Model for eco-score"""
        __tablename__ = 'eco-score'
        ecoScoreid = db.Column(db.Integer,
                        primary_key=True)
        userid = db.Column(db.Integer, db.ForeignKey('user.id'))
        ecoScore = db.Column(db.Integer(),
                                nullable=True,
                                unique=False)
        email = db.Column(db.String(40),
                        unique=True,
                        nullable=False)
        survey_responses = db.Column(db.Text)  # Store responses as a JSON string
        recommendations = db.Column(db.Text)  # Store recommendations as a JSON string



def set_responses(self, responses_dict):
        self.survey_responses = json.dumps(responses_dict)


def get_responses(self):
        return json.loads(self.survey_responses)


def set_recommendations(self, rec_dict):
        self.recommendations = json.dumps(rec_dict)


def get_recommendations(self):
         json.loads(self.recommendations)




















# class Event(db.Model):
#     __tablename__ = 'event'
#     eventID = db.Column(db.Integer, primary_key=True)
#     userID = db.Column(db.Integer, db.ForeignKey('user.userid'))
#     title = db.Column(db.String(80))
#     status = db.Column(db.String(80), default='active')
#     description = db.Column(db.String(389))
#     eventTime = db.Column(db.DateTime)
#     location = db.Column(db.String(80))

#     # Flair references
#     flairone_id = db.Column(db.Integer, db.ForeignKey('flair.flairID'))
#     flairtwo_id = db.Column(db.Integer, db.ForeignKey('flair.flairID'))
#     flarirthree_id = db.Column(db.Integer, db.ForeignKey('flair.flairID'))

#     # Relationships
#     flairone = db.relationship('Flair', foreign_keys=[flairone_id])
#     flairtwo = db.relationship('Flair', foreign_keys=[flairtwo_id])
#     flarirthree = db.relationship('Flair', foreign_keys=[flarirthree_id])

#     comments = db.relationship('Comment', backref='comments', lazy='dynamic')

#    def __repr__(self):
#        return '<Event %r>' % self.title


