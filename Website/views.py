from flask import Blueprint,render_template,request,flash
from flask.helpers import url_for
from flask_login import login_user,current_user,login_required
from sqlalchemy.sql.functions import user
import requests
from werkzeug.utils import redirect
views=Blueprint('views',__name__)
from . import db
from .models import Blog, User
import datetime
@views.route("/")
@login_required
def home():
    blogAll=Blog.query.all()
    blogAll=blogAll[::-1]
    blogLength=len(blogAll)
    author=[]
    for blog in blogAll:
        value=User.query.filter_by(id=blog.userId).first()
        author.append(value)
    return render_template("allblogs.html",blogs=blogAll,author=author,user=current_user,blogLength=blogLength)

@views.route("/writeBlog",methods=["GET","POST"])
def writeBlog():
    blogLength=len(current_user.blogs)
    if request.method=="POST":
        blog=request.form.get('blog')
        if len(blog)<=1:
            flash("Write a longer wit !",category='error')
        else:
            newBlogger=Blog(data=blog,userId=current_user.id)
            db.session.add(newBlogger)
            db.session.commit()
            blogLength=len(current_user.blogs)
            flash("Blog added!!",category='success')
    return render_template("home.html",user=current_user,length=blogLength)

@views.route("/bloggers")

def bloggers():
    users=User.query.all()
    return render_template("bloggers.html",users=users,user=current_user)


@views.route("/welcome")

def welcome():

    return render_template("welcome.html",user=current_user)

@views.route("/delete/<id>")

def deletePost(id):
    wit=Blog.query.filter_by(userId=id).first()
    if not wit:
        flash("Wit does not exist",category='error')
    else:
        db.session.delete(wit)
        db.session.commit()
        flash('Wit deleted',category='success')
    return redirect(url_for('views.home'))

@views.route("/profile/@/<id>")
@login_required
def displayProfile(id):
    displayUser=User.query.filter_by(id=id).first()
    return render_template("profile.html",user=displayUser)
