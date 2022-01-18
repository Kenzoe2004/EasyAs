import os
from flask import Blueprint, render_template, request, flash, redirect, url_for,Response
from werkzeug.utils import secure_filename, send_file
from flask_login import login_required, current_user
from .models import Post, User,Message,Comment,Chat_comment,Question_comment,Question
from . import db
from werkzeug.security import  check_password_hash
from os import path
from io import BytesIO
views = Blueprint("views", __name__)


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
    user=current_user
    if user.is_authenticated:
        flash("Hey you might wanna check for new messages",category='sucess')
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
        flash("You are banned.",category='error')
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

            post = Post(text=text, author=current_user.id,img_name=filename ,img=pic.read(),school=school,Course=Course)
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
        return send_file(BytesIO(post.img),download_name=post.img_name ,environ=request.environ, as_attachment=True)
    elif qn_id:
        qn = Question.query.filter_by(id=qn_id).first()
        return send_file(BytesIO(qn.img),download_name=qn.img_name ,environ=request.environ, as_attachment=True)
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
    image_file = url_for('static', filename=f'profile_pics/{current_user.profileimg}')
    if request.method == 'POST':
        user = current_user
        Namechange = request.form.get("userchange")
        if len(Namechange) < 2:
            image_file = url_for('static', filename=f'profile_pics/{current_user.profileimg}')
            flash('New Username too short!', category='error')
            return render_template('Userinfo.html', user=current_user,profilepic=image_file)
        username_exists = User.query.filter_by(username=Namechange).first()
        if username_exists:
            image_file = url_for('static', filename=f'profile_pics/{current_user.profileimg}')
            flash('Username taken!!', category='error')
            return render_template('Userinfo.html', user=current_user,profilepic=image_file)
        else:
            image_file = url_for('static', filename=f'profile_pics/{current_user.profileimg}')
            db.session()
            user.username = Namechange
            db.session.commit()
            flash('Username updated successfuly',category='success')
            return render_template('Userinfo.html', user=current_user,profilepic=image_file)
    else:
        return render_template('Userinfo.html', user=current_user,profilepic=image_file)


@views.route("/Admin")
@login_required
def Admin():

    id = current_user.id
    if id == 1:
        a = request.args.get('a')
        b = request.args.get('b')
        c = request.args.get('c')
        if a or b or c:
            posts = Post.query.filter(Post.text.contains(a), Post.school.contains(b), Post.Course.contains(c))
        else:
            posts = Post.query.all()
        return render_template('Admin.html', user=current_user,posts=posts)

    else:
        flash("Current user not a Admin",category='error')
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
        return render_template('Admin.html',posts = posts)
    else:
        return render_template('Admin.html')




@views.route("/change email", methods=['GET', 'POST'])
@login_required
def Newemail():
    if request.method == 'POST':
        password = request.form.get("password3")
        password2 = request.form.get("password4")
        user = current_user
        image_file = url_for('static', filename=f'profile_pics/{current_user.profileimg}')
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
                    flash('Email updated successfuly',category='success')
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
            picture_path = os.path.join(views.root_path, 'static/profile_pics', profilechange.filename)
            profilechange.save(picture_path)
            db.session()
            user.profileimg = str(profilechange.filename)
            db.session.commit()
            image_file = url_for('static', filename=f'profile_pics/{user.profileimg}')
            flash("File update successfull", category='sucess')
            flash("If file was not a ['png', 'jpg', 'jpeg', 'gif'] the file uploaded will not be displayed", category='error')
            return render_template('Userinfo.html', user=current_user, profilepic=image_file)
    else:
        image_file = url_for('static', filename=f'profile_pics/{current_user.profileimg}')
        return render_template('Profilepic.html', user=current_user, profilepic=image_file)


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
            message = Message(text=text, author2=current_user.id, username2=username2, sender=current_user.username)
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
    return render_template('View-message.html',user=current_user, messages=message,username2=current_user.username,sender=current_user.username)

@views.route("/view-sendmessages", methods=['GET', 'POST'])
@login_required
def view_sendmessage():
    message = Message.query.filter_by(author2=current_user.id)

    return render_template('View-message.html',user=current_user, messages=message,author2=current_user.id,sender=current_user.username)

@views.route("/chat/<id>", methods=['GET', 'POST'])
@login_required
def chat(id):
    message = Message.query.filter_by(id=id)
    return render_template('View-chat.html',id=id,user=current_user, messages=message,username2=current_user.username,sender=current_user.username)

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

    return redirect(url_for('views.chat',id=message_id))

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
       flash('deleted successfully',category='sucess')

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
        return render_template('Admin.html',posts = posts)
    else:
        return render_template('Admin.html')

@views.route("/users", methods=['GET', 'POST'])
@login_required
def view_users():
    c = request.args.get('c')
    if c:
        users = User.query.filter(User.username.contains(c))
        flash(f'These are all the users with the name {c}', category='success')
        return render_template('Find new friends.html', users=users )
    else:
        return render_template('Find new friends.html')




#def view_users():
    #c = request.args.get('c')
    #if c:
        #user = User.query.filter(User.username.contains(c)).first()
        #return render_template('Find new friends.html', user=user)
    #else:
        #user = current_user
        #return render_template('Find new friends.html', user=user)

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
        flash("You are banned.",category='error')
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
            question = Question(text=text, author=current_user.id,img_name=filename ,img=pic.read(),school=school,Course=Course)

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

    return redirect(url_for('views.view_Questions',id=question_id))

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
       flash('deleted successfully',category='sucess')

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
            flash(f'These are all the users with the name {c}', category='success')
            return render_template('Admin-Finder.html', users=users )
        else:
            return render_template('Admin-Finder.html')

    else:
        flash("Current user not a Admin", category='error')
        return redirect(url_for('views.home'))
