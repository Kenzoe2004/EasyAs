from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    userimposterid = db.Column(db.Integer,default=0)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
    profileimg = db.Column(db.String(20), nullable=False, default='Userinfoimage.png')
    messages = db.relationship('Message', backref='user', passive_deletes=True)
    chat_comments = db.relationship('Chat_comment', backref='user', passive_deletes=True)
    question_comments = db.relationship('Question_comment', backref='user', passive_deletes=True)
    questions = db.relationship('Question', backref='user', passive_deletes=True)

    @staticmethod
    def is_authenticated(self):
        return True



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    img_name = db.Column(db.Text, nullable=False)
    img = db.Column(db.LargeBinary, nullable=False) 
    Course = db.Column(db.Text, nullable=False)
    school = db.Column(db.Text, nullable=False)
    comments = db.relationship('Comment', backref='post', passive_deletes=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete="CASCADE"), nullable=False)

# class Img(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     img = db.Column(db.Text, nullable=False)
#     name = db.Column(db.Text, nullable=False)
#     mimetype = db.Column(db.Text, nullable=False)
#     db.relationship('Post', backref='img', passive_deletes=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    sender=db.Column(db.Text, unique=False)
    username2 = db.Column(db.Text, unique=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author2 = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    comments = db.relationship('Chat_comment', backref='message', passive_deletes=True)

class Chat_comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    message_id = db.Column(db.Integer, db.ForeignKey(
        'message.id', ondelete="CASCADE"), nullable=False)

class Question_comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey(
        'question.id', ondelete="CASCADE"), nullable=False)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    img = db.Column(db.LargeBinary, nullable=False)
    Course = db.Column(db.Text, nullable=False)
    school = db.Column(db.Text, nullable=False)
    comments = db.relationship('Question_comment', backref='question', passive_deletes=True)
