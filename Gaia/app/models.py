
from datetime import datetime
from flask_login import UserMixin
import pytz
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
    firstname = db.Column(db.String(40),
                         nullable=False)
    lastname = db.Column(db.String(40),
                         nullable=False)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.now(pytz.timezone('US/Eastern')))
    ismod = db.Column(db.Boolean,
                           default=False)
    
    # #Attributes for the user's profile
    # madeProfileAlready = db.Column(db.Boolean,
    #                                default=False)
    # pronouns = db.Column(db.String(40))
    # aboutMe = db.Column(db.String(500),
    #                      primary_key=False, unique=False, nullable=False)
    # myMajor = db.Column(db.String(40),
    #                      nullable=False)
    # academicYear = db.Column(db.String(40),
    #                           nullable=False)
    # socialMediaLink = db.Column(db.String(255),
    #                              nullable=True)
    
    def get_id(self):
            return (self.userid)
        
    #ADD THESE LATER
    posts = db.relationship('Event', backref='author', lazy='dynamic')
    
    #NOT NEEDED: if you need all the comments of the user, user query the Comment table with userID
    #comments = db.relationship('Comment', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)



class Event(db.Model):
    __tablename__ = 'event'
    eventID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userid'))
    title = db.Column(db.String(80))
    status = db.Column(db.String(80), default='active')
    description = db.Column(db.String(389))
    eventTime = db.Column(db.DateTime)
    location = db.Column(db.String(80))

    # Flair references
    flairone_id = db.Column(db.Integer, db.ForeignKey('flair.flairID'))
    flairtwo_id = db.Column(db.Integer, db.ForeignKey('flair.flairID'))
    flarirthree_id = db.Column(db.Integer, db.ForeignKey('flair.flairID'))

    # Relationships
    flairone = db.relationship('Flair', foreign_keys=[flairone_id])
    flairtwo = db.relationship('Flair', foreign_keys=[flairtwo_id])
    flarirthree = db.relationship('Flair', foreign_keys=[flarirthree_id])

    comments = db.relationship('Comment', backref='comments', lazy='dynamic')

    def __repr__(self):
        return '<Event %r>' % self.title


class Flair(db.Model):
    __tablename__ = 'flair'
    flairID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __repr__(self):
        return f'{self.name}'




class RSVP(db.Model):
     __tablename__ = 'rsvp'
     rsvpID = db.Column(db.Integer, primary_key=True)
     userID = db.Column(db.Integer, db.ForeignKey('user.userid'))
     eventID = db.Column(db.Integer, db.ForeignKey('event.eventID'))
     timestamp = db.Column(db.DateTime)
     __table_args__ = (UniqueConstraint('userID', 'eventID', name='unique_rsvp_per_user_event'),)
    
    

     def __repr__(self):
         return '<RSVP %r>' % self.rsvpID


class Comment(db.Model):
     __tablename__ = 'comment'
     commentID = db.Column(db.Integer, primary_key=True)
     userID = db.Column(db.Integer, db.ForeignKey('user.userid'))
     eventID = db.Column(db.Integer, db.ForeignKey('event.eventID'))
     message = db.Column(db.String(255))
     timestamp = db.Column(db.DateTime, default=datetime.now(pytz.timezone('US/Eastern')))

     author = db.Relationship('User', backref='author', lazy='joined') 

     def __repr__(self):
         return '<Comment %r>' % self.message

        


