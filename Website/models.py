from enum import unique
from . import db

from flask_login import UserMixin

from sqlalchemy.sql import func

class Blog(db.Model):
      id=db.Column(db.Integer,primary_key=True)
      data=db.Column(db.String(10000))
      date=db.Column(db.DateTime(timezone=True),default=func.now())
      userId=db.Column(db.Integer,db.ForeignKey('user.id'))


class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(100),unique=True)
    phoneNumber=db.Column(db.String(10),unique=True)
    password=db.Column(db.String(100))
    firstName=db.Column(db.String(100))
    lastName=db.Column(db.String(100))
    blogs=db.relationship('Blog')