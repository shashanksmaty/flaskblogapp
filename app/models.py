from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(128), nullable=False)
    posts = db.relationship('Post', backref='users', lazy=True)

    def __init__(self, email, username, image_file, password):
        self.email = email
        self.username = username
        self.image_file = image_file
        self.password = password

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, title, date_posted, content, user_id):
        self.title = title
        self.date_posted = date_posted
        self.content = content
        self.user_id = user_id

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
