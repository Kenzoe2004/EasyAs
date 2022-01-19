import email
import os
from flask import Blueprint, render_template, request, flash, redirect, url_for, Response
from werkzeug.utils import secure_filename, send_file
from flask_login import login_required, current_user
from .models import Post, User, Message, Comment, Chat_comment, Question_comment, Question
from . import db
from werkzeug.security import check_password_hash
from os import path
from io import BytesIO
import pyrebase
import threading


views = Blueprint("views", __name__)

config = {
    "apiKey": "AIzaSyBUPHX8nHL4DwCSHZhvoJpsR0aeWuSrFvc",
    "authDomain": "easyas-edcdf.firebaseapp.com",
    "projectId": "easyas-edcdf",
    "storageBucket": "easyas-edcdf.appspot.com",
    "messagingSenderId": "104832045862",
    "appId": "1:104832045862:web:0685a5a1deb61822a927e7",
    "measurementId": "G-SPNCHMPQKS",
    "serviceAccount": {
        "type": "service_account",
        "project_id": "easyas-edcdf",
        "private_key_id": "c55ec5e4e63cb40ef7c6638ed988e2897377315a",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC6dJRNQuaO2/0g\nCsBc5ykpxcMKKg4hwexPRTkjQ0zg4OMFRKAiHc0fcDJrN3K2GVVeGO1ZlIHfZ/Qv\nawxePO3HiLAtvOLLnpENylIdiDUNTpRb2FmUZ7GOjIgV13AFdvZ4gGlUCc4X79Gn\n3Ij85pnaSRv0JZoPhdiBWBkZkMI2Cim6/Cpp5uVt/fiWnAvLAbSBS4guz4xlutdH\nnyogjBzSdb5AzJCVJxoMshd+L/8/Ep4Xom5UrGRZP9SzLxgUfmr2AwaUq+umqQXd\nj/uPPSoWzxV1dVWIBeJbGf5R2XqYihntvn06GltlXHv/iFhx6Eo74F41oSgSQkRo\n1EUQgQUhAgMBAAECggEAC12t6KPKYC0C2iAtp7wjozs973Gu2Nn0aMSkfgTNO+wZ\niqmrRUkhxufU+vovUPBsZscIOOy3mgHBPd69q0T1jbNEYhVgkd8BoqCRruEtsrj2\njD68/zHu/eyNIx+14W9mCORzBz9tw8HHuv7Tju8Ts92/CXv9TzLuhrvzE77iR97t\n2QM5DLlrLGar7wPrEJFnObRLaBdiQUbKs1hWarua6LfsB1pnD8kwT263qhy1Rtlc\n8jJJ8ebN4Ck4xBDrknZ3XlIKYkM3eV8OY+WCGggC/L+QIMnnN+ByfSP+AtEuyT55\nKz6Wsv/jZ/mLYH/2abeHVqz39Gj24KhbZMuQ7MfEHQKBgQD6GLsBAaCH14FCHs1G\nI9a0VQ4UVkwI2M/HSO/ceb77RD2C55CESNMHoe6PXBXc1FLvP+gDaEKjyHPEueQt\nP2f3owlBGMFiSzgmSy3clfMUbij4f+6zJHq9okJe7VVJhpq9PYuXbyRq9vdgNbxE\nHrcLN6BuxVojANvXYw6u1tPeQwKBgQC+20gDquNeTeTzG5seTwchCfzqsIqKXV4m\n3NkZSypTlNSq5PczDfZhc7u1MUPjxmgI1uFOI6qNLPQ+zEOzDuKvQK/HIXXtegmH\nBCHI4TAhh2uNRNrmMx7THEOGF905b+yEHZldhVUCD+FF8zw5o9959QsHYVoY5JfU\nDbhnfRvCywKBgHQ5Oe5lyyxVwgPwPITz8rsrK7fXws35s9Vw18cl7NLoC43h/w76\nqNdLMYn9yUsugLwefrvWn+FtLh+mI5vDc5VpdsuBrZz4R8fD+DQimyxLZU7WZR9r\nPH8UALQMpy3cF90J1O0zAUGUM7HKRwuBGp9j4nKX1COgKooVxqUJwLvxAoGAa4Dy\nsHYqei0gIDvVhR34owiQONXWQ5fR98wAUXoATnIP1G8COvTLahsZiTdFyWAxq4D2\nCeCXKcw/i7vdClgBIbwrBtx3I5vREAcozJDjXo976mf1cSMsYreR5U894iOEMurF\nP2Nh/bZaKt+WddUzhOudGbwhVtI0H1LXIxvabj8CgYEAl8LEVjkUHoxVrUhswDzO\no1tgPmdGxj8kmc/J6tf7w0vkTbE6+wYWG2g5XeNxxoPx+ZNPeDxuy3J0Qy9O4mcX\nfny92gaW3EXO/GpRsU0f21VUTo9qGnoZtj4IsLJDFWiKsqfY6D78853L3VXeCthL\nktDrnbldFYFakZLTKrFIICo=\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-6wuiq@easyas-edcdf.iam.gserviceaccount.com",
        "client_id": "116874794661608759169",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-6wuiq%40easyas-edcdf.iam.gserviceaccount.com"
    },
    "databaseURL": "gs://easyas-edcdf.appspot.com"
}
firebase_storage = pyrebase.initialize_app(config)
auth = firebase_storage.auth()

email = "easyas2004@gmail.com"
password = "%easyasfirebase"

firebase_user = auth.sign_in_with_email_and_password(email, password)
idToken  = firebase_user['idToken']
storage = firebase_storage.storage()

def refresh_firebase_token():
    global idToken, firebase_user
    firebase_user = auth.refresh(firebase_user['refreshToken'])
    idToken  = firebase_user['idToken']
    return

start_time = threading.Timer(2700,refresh_firebase_token)
start_time.start()

@views.route("/intropage")
def intro():
    return render_template('Intro.html')

@views.route("/About-us")
def About():
    return render_template('About-Us.html')

@views.route("/")
@views.route("/home")
# @login_required
def home():
    user = current_user
    if user.is_authenticated:
        flash("Hey you might wanna check for new messages", category='sucess')
        q = request.args.get('q')
        if q:
            posts = Post.query.filter(Post.text.contains(q))
        else:
            posts = Post.query.all()
        return render_template("home.html", user=current_user, posts=posts)
    else:
        return render_template('Intro.html')


@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if User.query.filter_by(username=current_user.username).first().userimposterid == 1:
        flash("You are banned.", category='error')
        return redirect(url_for('auth.logout'))
    if request.method == "POST":
        text = request.form.get('text')
        pic = request.files['pic']
        school = request.form.get('school').lower()
        Course = request.form.get('Course').lower()

        if not text and not Course and not school:
            flash('Post cannot be empty', category='error')
        else:
            filename = secure_filename(pic.filename)

            post = Post(text=text, author=current_user.id, img_name=filename,
                        img=pic.read(), school=school, Course=Course)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('create-post.html', user=current_user)


@views.route("/download")
@login_required
def download():
    post_id = request.args.get('postid')
    qn_id = request.args.get('qnid')
    if post_id:
        post = Post.query.filter_by(id=post_id).first()
        if len(post.img)>0:
            return send_file(BytesIO(post.img), download_name=post.img_name, environ=request.environ, as_attachment=True)
        else:
            return redirect(url_for('views.home'))
    elif qn_id:
        qn = Question.query.filter_by(id=qn_id).first()
        if len(qn.img)>0:
            return send_file(BytesIO(qn.img), download_name=qn.img_name, environ=request.environ, as_attachment=True)
        else:
            return redirect(url_for('views.home'))
    else:
        return redirect(url_for('views.home'))


@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    comment = Comment.query.filter_by(post_id=id).first()

    if not post:
        flash("Post does not exist.", category='error')
    if current_user.id == 1:
        for comment in post.comments:
            db.session.delete(comment)
            db.session.commit()
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')
    elif current_user.id != post.author:
        flash('You do not have permission to delete this post.', category='error')
    else:
        for comment in post.comments:
            db.session.delete(comment)
            db.session.commit()
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')
    return redirect(url_for('views.home'))


@views.route("/show")
@login_required
def show():
    a = request.args.get('a')
    b = request.args.get('b')
    c = request.args.get('c')
    if a or b or c:
        posts = Post.query.filter(Post.text.contains(a),Post.school.contains(b.lower()),Post.Course.contains(c.lower()))
    else:
        posts = Post.query.all()
    return render_template('Show.html', user=current_user, posts=posts)


@views.route("/userinfo", methods=['GET', 'POST'])
@login_required
def userinfo():
    image_file = current_user.profile_img_url
    if request.method == 'POST':
        user = current_user
        Namechange = request.form.get("userchange")
        if len(Namechange) < 2:
            image_file = current_user.profile_img_url
            flash('New Username too short!', category='error')
            return render_template('Userinfo.html', user=current_user, profilepic=image_file)
        username_exists = User.query.filter_by(username=Namechange).first()
        if username_exists:
            image_file = current_user.profile_img_url
            flash('Username taken!!', category='error')
            return render_template('Userinfo.html', user=current_user, profilepic=image_file)
        else:
            image_file = current_user.profile_img_url
            db.session()
            user.username = Namechange
            db.session.commit()
            flash('Username updated successfuly', category='success')
            return render_template('Userinfo.html', user=current_user, profilepic=image_file)
    else:
        return render_template('Userinfo.html', user=current_user, profilepic=image_file)


@views.route("/Admin")
@login_required
def Admin():

    id = current_user.id
    if id == 1:
        a = request.args.get('a')
        b = request.args.get('b')
        c = request.args.get('c')
        if a or b or c:
            posts = Post.query.filter(Post.text.contains(
                a), Post.school.contains(b), Post.Course.contains(c))
        else:
            posts = Post.query.all()
        return render_template('Admin.html', user=current_user, posts=posts)

    else:
        flash("Current user not a Admin", category='error')
    return redirect(url_for('views.home'))


@views.route("/Admin-delete/<author>")
@login_required
def Admindelete(author):
    user = User.query.filter_by(id=author).first()
    if user:
        db.session()
        user2 = user.userimposterid
        user.userimposterid = 1
        db.session.commit()
        posts = Post.query.all()
        return render_template('Admin.html', posts=posts)
    else:
        return render_template('Admin.html')


@views.route("/change email", methods=['GET', 'POST'])
@login_required
def Newemail():
    if request.method == 'POST':
        password = request.form.get("password3")
        password2 = request.form.get("password4")
        user = current_user
        image_file = current_user.profile_img_url
        emailchange = request.form.get("emailchange")
        if password != password2:
            flash('Password don\'t match!', category='error')
            return render_template('Userinfo.html', user=current_user, profilepic=image_file)

        else:
            if check_password_hash(user.password, password):
                if len(emailchange) < 4:
                    flash('New email too short!', category='error')
                    return render_template('Userinfo.html', user=current_user, profilepic=image_file)
                email_exists = User.query.filter_by(email=emailchange).first()
                if email_exists:
                    flash('email taken!!', category='error')
                    return render_template('Userinfo.html', user=current_user, profilepic=image_file)
                else:
                    db.session()
                    user.email = emailchange
                    db.session.commit()
                    flash('Email updated successfuly', category='success')
                    return render_template('Userinfo.html', user=current_user, profilepic=image_file)
    else:
        return render_template('New-email.html', user=current_user)


@views.route("/change profilepic", methods=['GET', 'POST'])
@login_required
def Profile():
    if request.method == 'POST':
        user = current_user
        profilechange = request.files["profilepic"]
        if not profilechange:
            flash('New  too short!', category='error')
            return render_template('Profilepic.html', user=current_user)
        else:
            db.session()
            filename = secure_filename(profilechange.filename)
            filename = filename.split('.')

            storage.child("profile_pic").child(f"{current_user.id}.{filename[len(filename)-1]}").put(profilechange)
            user.profile_img = profilechange.filename
            url = storage.child("profile_pic").child(f"{current_user.id}.{filename[len(filename)-1]}").get_url(idToken)
            user.profile_img_url = url
            db.session.commit()
            
            flash("File update successfull", category='sucess')
            return redirect(url_for('views.userinfo'))
    else:
        user = current_user
        return render_template('Profilepic.html', user=current_user, profilepic=user.profile_img_url)


@views.route("/create-message", methods=['GET', 'POST'])
@login_required
def create_message():
    if request.method == "POST":
        text = request.form.get('text')
        username2 = request.form.get('username2')
        username_exists = User.query.filter_by(username=username2).first()

        if not text:
            flash('message cannot be empty', category='error')
        if not username2:
            flash('message cannot be empty', category='error')
        if username_exists:
            message = Message(text=text, author2=current_user.id,
                              username2=username2, sender=current_user.username)
            db.session.add(message)
            db.session.commit()
            flash('message created!', category='success')
            return redirect(url_for('views.home'))

        else:
            flash('Usernot found!', category='error')

    return render_template('create-messages.html', user=current_user)


@views.route("/view-messages", methods=['GET', 'POST'])
@login_required
def view_message():
    message = Message.query.filter_by(username2=current_user.username)
    return render_template('View-message.html', user=current_user, messages=message, username2=current_user.username, sender=current_user.username)


@views.route("/view-sendmessages", methods=['GET', 'POST'])
@login_required
def view_sendmessage():
    message = Message.query.filter_by(author2=current_user.id)

    return render_template('View-message.html', user=current_user, messages=message, author2=current_user.id, sender=current_user.username)


@views.route("/chat/<id>", methods=['GET', 'POST'])
@login_required
def chat(id):
    message = Message.query.filter_by(id=id)
    return render_template('View-chat.html', id=id, user=current_user, messages=message, username2=current_user.username, sender=current_user.username)


@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')

    return redirect(url_for('views.home'))


@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.home'))


@views.route("/create-chat/<message_id>", methods=['POST'])
@login_required
def create_chatcomment(message_id):
    text = request.form.get('text')
    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        message = Message.query.filter_by(id=message_id)
        if message:
            chat_comment = Chat_comment(
                text=text, author=current_user.id, message_id=message_id)
            db.session.add(chat_comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')

    return redirect(url_for('views.chat', id=message_id))


@views.route("/delete-chat/<chat_comment_id>")
@login_required
def delete_chat(chat_comment_id):
    comment = Chat_comment.query.filter_by(id=chat_comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()
        flash('deleted successfully', category='sucess')

    return redirect(url_for('views.view_message'))


@views.route("/delete_message/<id>")
@login_required
def delete_message(id):
    message = Message.query.filter_by(id=id).first()
    chat_comment = Chat_comment.query.filter_by(message_id=id).first()

    if not message:
        flash("Post does not exist.", category='error')

    else:
        for chat_comment in message.comments:
            db.session.delete(chat_comment)
            db.session.commit()
        db.session.delete(message)
        db.session.commit()
        flash('message deleted.', category='success')
    return redirect(url_for('views.view_message'))


@views.route("/Admin-undelete/<author>")
@login_required
def AdminUndelete(author):
    user = User.query.filter_by(id=author).first()
    if user:
        db.session()
        user2 = user.userimposterid
        user.userimposterid = 0
        db.session.commit()
        posts = Post.query.all()
        return render_template('Admin.html', posts=posts)
    else:
        return render_template('Admin.html')


@views.route("/users", methods=['GET', 'POST'])
@login_required
def view_users():
    c = request.args.get('c')
    if c:
        users = User.query.filter(User.username.contains(c))
        flash(f'These are all the users with the name {c}', category='success')
        return render_template('Find new friends.html', users=users)
    else:
        return render_template('Find new friends.html')


# def view_users():
    #c = request.args.get('c')
    # if c:
        #user = User.query.filter(User.username.contains(c)).first()
        # return render_template('Find new friends.html', user=user)
    # else:
        #user = current_user
        # return render_template('Find new friends.html', user=user)

@views.route("/Tests")
@login_required
def view_Questions():
    a = request.args.get('a')
    b = request.args.get('b')
    c = request.args.get('c')
    if a or b or c:
        questions = Question.query.filter(Question.text.contains(a), Question.school.contains(b.lower()),Question.Course.contains(c.lower()))
    else:
        questions = Question.query.all()
    return render_template('Question.html', user=current_user, Questions=questions)


@views.route("/create-question", methods=['GET', 'POST'])
@login_required
def create_Questions():
    if User.query.filter_by(username=current_user.username).first().userimposterid == 1:
        flash("You are banned.", category='error')
        return redirect(url_for('auth.logout'))
    if request.method == "POST":
        text = request.form.get('text')
        pic = request.files['pic']
        school = request.form.get('school').lower()
        Course = request.form.get('Course').lower()

        if not text and not Course and not school:
            flash('Post cannot be empty', category='error')
        else:
            filename = secure_filename(pic.filename)
            question = Question(text=text, author=current_user.id,
                                img_name=filename, img=pic.read(), school=school, Course=Course)

            db.session.add(question)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.view_Questions'))

    return render_template('create-question.html', user=current_user)


@views.route("/create-question/<question_id>", methods=['POST'])
@login_required
def create_questioncomment(question_id):
    text = request.form.get('text')
    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        message = Message.query.filter_by(id=question_id)
        if message:
            comment = Question_comment(
                text=text, author=current_user.id, question_id=question_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')

    return redirect(url_for('views.view_Questions', id=question_id))


@views.route("/delete-questionchat/<question_comment_id>")
@login_required
def delete_questionchat(question_comment_id):
    comment = Question_comment.query.filter_by(id=question_comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()
        flash('deleted successfully', category='sucess')

    return redirect(url_for('views.view_Questions'))


@views.route("/delete-question/<id>")
@login_required
def delete_question(id):
    question = Question.query.filter_by(id=id).first()
    comment = Comment.query.filter_by(post_id=id).first()

    if not question:
        flash("Post does not exist.", category='error')
    if current_user.id == 1:
        for question_comments in question.comments:
            db.session.delete(question_comments)
            db.session.commit()
        db.session.delete(question)
        db.session.commit()
        flash('Post deleted.', category='success')
    elif current_user.id != question.author:
        flash('You do not have permission to delete this post.', category='error')
    else:
        for question_comments in question.comments:
            db.session.delete(question_comments)
            db.session.commit()
        db.session.delete(question)
        db.session.commit()
        flash('Post deleted.', category='success')
    return redirect(url_for('views.view_Questions'))


@views.route("/posts/<author>")
@login_required
def posts_user(author):
    user = current_user
    if user.is_authenticated:
        flash("Hey you might wanna check for new messages", category='sucess')
        q = request.args.get('q')
        if q:
            posts = Post.query.filter(Post.text.contains(q))
        else:
            posts = Post.query.filter_by(author=author)
        return render_template("Users-post.html", user=current_user, posts=posts)
    else:
        return render_template('Intro.html')


@views.route("/user-questions/<author>")
@login_required
def view_UsersQuestions(author):
    questions = Question.query.filter_by(author=author)
    return render_template('User-Questions.html', user=current_user, Questions=questions)


@views.route("/Admin-search", methods=['GET', 'POST'])
@login_required
def view_Adminusers():
    id = current_user.id
    if id == 1:
        c = request.args.get('c')
        if c:
            users = User.query.filter(User.username.contains(c))
            flash(
                f'These are all the users with the name {c}', category='success')
            return render_template('Admin-Finder.html', users=users)
        else:
            return render_template('Admin-Finder.html')

    else:
        flash("Current user not a Admin", category='error')
        return redirect(url_for('views.home'))
