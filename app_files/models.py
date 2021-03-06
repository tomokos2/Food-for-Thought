from app_files import db
from datetime import datetime
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Length, Email
from flask_wtf.file import FileAllowed, FileField


# Database model for Post
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_path = db.Column(db.String(200))
    # user.id is lowercase because referencing the table name, which is user by default
    author = db.Column(db.String(100), db.ForeignKey('user.username'), nullable=False)

    comments = db.relationship('Comment', backref='post_src', lazy=True)

    def __repr__(self):
        return f'<Post: id={self.id}, title={self.title} author={self.author}>'


# Database model for User that also implemenets flask-login
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    # Relationship to post model
    # lazy means sqlalchemy will load all of the data in one go
    posts = db.relationship('Post', backref='post_author', lazy=True, order_by='Post.date.desc()')

    def __repr__(self):
        return f'<User: id={self.id}, name={self.username}>'


# Database model for every comment
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # The author of the comment
    author = db.Column(db.String(100), db.ForeignKey('user.username'), nullable=False)
    # The post under which the comment was written
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f'<Comment: id={self.id}, content={self.content[0:20]}>'


# Wtform for Logging in to the app
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=20)])
    shouldRemember = BooleanField('Remember Me')


# Wtform for Registering for the app
class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid Email'), Length(min=4, max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=20)])
    passwordRetype = PasswordField('Retype Your Password', validators=[InputRequired(), Length(min=4, max=20)])


# Wtform for creating a new post
class PostForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(min=1, max=40)])
    # An optional image
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    content = TextAreaField('Content', validators=[InputRequired(), Length(min=1, max=2000)])


# Wtform for making a comment on a post
class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[InputRequired(), Length(min=1, max=400)])


# Wtform for editing a post
class EditForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(min=1, max=40)])
    content = TextAreaField('Content', validators=[InputRequired(), Length(min=1, max=2000)])



