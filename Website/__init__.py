from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager
import socketio
from sqlalchemy.orm import query

from flask_socketio import SocketIO,send


db=SQLAlchemy()

DB_NAME="database.db"
from os import path


def createApp():
    app=Flask(__name__)
    app.config['SECRET_KEY']='adflsbvgaj'
    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'
    db.init_app(app)
    from .views import views
    from .auth import auth
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    from .models import User,Blog

    createDB(app)

    login_manager=LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def loadUser(id):
         return User.query.get(int(id))


    return app

def createDB(app):
    if not path.exists('Website/'+DB_NAME):
        db.create_all(app=app)
        print('Created db')

