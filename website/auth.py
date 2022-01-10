from flask import Blueprint, render_template, redirect, url_for
from flask import Blueprint, render_template, redirect, url_for, request, flash
import flask
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

auth = Blueprint("auth", __name__)
otp_dict = {}

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if user.id!=1:
                if user.userimposterid == 1:
                    flash("Account id Baned", category='error')
                    return render_template("login.html", user=current_user)
            if check_password_hash(user.password, password):
                flash("Logged in!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route("/sign-up", methods=['GET'])
def sign_up():
    return render_template("signup.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))

@auth.route("/verify", methods=['POST'])
def verify():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            flash('Email is already in use.', category='error')
            return render_template("signup.html")
        elif username_exists:
            flash('Username is already in use.', category='error')
            return render_template("signup.html")
        elif password1 != password2:
            flash('Password don\'t match!', category='error')
            return render_template("signup.html")
        elif len(username) < 2:
            flash('Username is too short.', category='error')
            return render_template("signup.html")
        elif len(password1) < 6:
            flash('Password is too short.', category='error')
            return render_template("signup.html")
        elif len(email) < 4:
            flash("Email is invalid.", category='error')
            return render_template("signup.html")
        else:
            otp = random.randint(1111,9999)
            sender_address = 'easyas2004@gmail.com'
            sender_pass = '%easyaakash'
            mail_content = f'''
                            Dear {email},\n
                            Please use the one-time verification code '{otp}' to verify your account and login to your EasyAs Dashboard.\n
                            This verification code is valid for 5 minutes. Do not share your OTP or credentials with anyone on call, email or messages.\n\n
                            For any queries or concerns, write to us at {sender_address}.\n\n
                            Regards,\n
                            Team,\n
                            EasyAs'''
            message = MIMEMultipart()
            message['From'] = sender_address
            message['To'] = email
            message['Subject'] = 'Email Verification :: Easy As :)'   #The subject line
            message.attach(MIMEText(mail_content, 'plain'))
            #Create SMTP session for sending the mail
            session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
            session.starttls() #enable security
            session.login(sender_address, sender_pass) #login with mail_id and password
            text = message.as_string()
            session.sendmail(sender_address, email, text)
            otp_dict[email] = otp
            session.quit()
        flash('Please refer to your email ID for verification code.', category='success')
        return render_template("verify.html",email = email, username = username, password1 = password1)
@auth.route("/verify-1", methods=['POST'])
def verify1():
    if request.method == 'POST':
        otp_user = request.form.get("otp")
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        if otp_user.isdigit():
            if int(otp_user) == otp_dict[email]:
                otp_dict.pop(email)
                new_user = User(email=email, username=username, password=generate_password_hash(
                password, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash('User created!')
                return redirect(url_for('views.home'))
            else:
                flash('OTP is incorrect.', category='error')
                return render_template("verify.html", email = email, username = username, password1 = password)
        else:
            flash('OTP is incorrect.', category='error')
            return render_template("verify.html", email = email, username = username, password1 = password)