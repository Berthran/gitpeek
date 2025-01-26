'''
Tables of the Database
'''
from sqlalchemy.dialects.postgresql import ARRAY # type: ignore
from datetime import datetime
from gitspeak import db # type: ignore



class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    access_token = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True)
    profile = db.relationship('Profile', back_populates='user', uselist=False, lazy=True)
    posts = db.relationship('Post', back_populates='author', lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    profile_picture = db.Column(db.String(255), default='default.jpg')
    skill_level = db.Column(db.String(120))
    tech_skill = db.Column(db.String(120))
    job_type = db.Column(db.String(120))
    job_goals = db.Column(ARRAY(db.String(120)), nullable=True)
    user = db.relationship('User', back_populates='profile', lazy=True)
    
    
    def __repr__(self):
        return f"Profile('{self.user}', '{self.profile_picture}')"


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    linkedin_post = db.Column(db.Text, nullable=False)
    twitter_post = db.Column(db.Text, nullable=False)
    post_type = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = db.relationship('User', back_populates='posts', lazy=True)
    
    def __repr__(self):
        return f"Post('{self.author}', '{self.title}', '{self.date_posted}')"

