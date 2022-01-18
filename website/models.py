from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

default_img_url = "https://firebasestorage.googleapis.com/v0/b/easyas-edcdf.appspot.com/o/profile_pic%2Fdefault_pic?alt=media&token=eyJhbGciOiJSUzI1NiIsImtpZCI6IjQwMTU0NmJkMWRhMzA0ZDc2NGNmZWUzYTJhZTVjZDBlNGY2ZjgyN2IiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZWFzeWFzLWVkY2RmIiwiYXVkIjoiZWFzeWFzLWVkY2RmIiwiYXV0aF90aW1lIjoxNjQyNDU2NTY5LCJ1c2VyX2lkIjoiaFdmVzg4RGR4YlVmNDZPY3JPbjBKSGVBc1BLMiIsInN1YiI6ImhXZlc4OERkeGJVZjQ2T2NyT24wSkhlQXNQSzIiLCJpYXQiOjE2NDI0NTY1NjksImV4cCI6MTY0MjQ2MDE2OSwiZW1haWwiOiJlYXN5YXMyMDA0QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbImVhc3lhczIwMDRAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.spThUdE5eJDdVT7P_lMUD_FT5cyWF9c-vKZ9-qFaUL6qrJrI4gCOtRSFLG1oNOnh4lZZGfQV1ruui7OdiXlorUzlKRsltV3qK5Afm8C5g2mIV7nifAUSJYSZVDBhWnNAuLPFfgoT3YyprEDtI05WjoUfdiafW-sxpQ1EtgZ3e8qxPYSHPXvs44jMYWux_ytiHBQnqC8dGXXoFCPUfJBNYHEAet8hiahsMwdgf56KqOX-taV1ege3QD5bA6N9WDmOCrfMI27e6LjuHhm0HrABrgJ1k6Qn5i8OvnkBernfbJ2WGzjMSXF67_qea8O6ST9ab0RIPqv-PsDbgGhbJk5QMA"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    userimposterid = db.Column(db.Integer,default=0)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
    profile_img = db.Column(db.String(150), nullable=False) 
    profile_img_url = db.Column(db.String(150), nullable=False, default=default_img_url) 
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
    img_name = db.Column(db.Text, nullable=False)
    img = db.Column(db.LargeBinary, nullable=False)
    Course = db.Column(db.Text, nullable=False)
    school = db.Column(db.Text, nullable=False)
    comments = db.relationship('Question_comment', backref='question', passive_deletes=True)
