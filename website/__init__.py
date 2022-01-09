from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()

ENV = 'DEP'
DB_NAME = 'database.db'
URL = 'postgresql://uyfdoacixjhlgx:97f99901a2e54cea748bb32960523cdf589912e58b213f4660058c4b9a5644ef@ec2-54-196-105-177.compute-1.amazonaws.com:5432/d8p6moob0r03gl'



def create_app():
    if ENV == 'DEV':
        app = Flask(__name__)
        app.config['SECRET_KEY'] = "helloworld"
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_NAME
        db.init_app(app)
    else:
        app = Flask(__name__)
        app.config['SECRET_KEY'] = "helloworld"
        app.config['SQLALCHEMY_DATABASE_URI'] = URL
        db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Post,Img

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if ENV == 'DEV':
        if not path.exists("website/" + DB_NAME):
            db.create_all()
            print("Created database!")
    else:
        if not path.exists("website/" + URL):
            db.create_all(app=app)
            print("Created database!")

