from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class Hero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(200), nullable=False)  # path to profile image


class About(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.Text, nullable=False)  # narrative-style bio
    profile_image = db.Column(db.String(200), nullable=True)  # optional separate photo


class CreativeWriting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    link = db.Column(db.String(250), nullable=True)  # link to external essay (Afrocritik, Substack)
    image = db.Column(db.String(200), nullable=True)  # optional image for the essay


class ContentWriting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    link = db.Column(db.String(250), nullable=True)  # link to sample work or case study
    image = db.Column(db.String(200), nullable=True)  # optional image for the project


class Leadership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(150), nullable=False)
    organization = db.Column(db.String(150), nullable=True)
    year = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)


class Advocacy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(200), nullable=True)  # optional for campaign visuals


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    impact = db.Column(db.Text, nullable=True) 
    link = db.Column(db.String(250), nullable=True) # optional for outcomes
    image = db.Column(db.String(200), nullable=True)
     # project photo


class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    video_url = db.Column(db.String(250), nullable=False)  # YouTube/Instagram embed link
    thumbnail = db.Column(db.String(200), nullable=True)  # optional thumbnail image

class Volunteering(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organization = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(150), nullable=True)
    year = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(200), nullable=True)  # optional logo/photo


class ContactInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False)
    instagram = db.Column(db.String(150), nullable=True)
    substack = db.Column(db.String(150), nullable=True)
    linkedin = db.Column(db.String(150), nullable=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
