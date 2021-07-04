from flask import Blueprint,render_template,request,flash
from flask_login import login_user,current_user,login_required
from sqlalchemy.sql.functions import user
import requests
views=Blueprint('views',__name__)
from . import db
from .models import Blog, User

@views.route("/")
@login_required
def home():
    blogAll=Blog.query.all()
    blogAll=blogAll[::-1]
    blogLength=len(blogAll)
    author=[]
    for blog in blogAll:
        author.append(User.query.filter_by(id=blog.userId).first())
    return render_template("allblogs.html",blogs=blogAll,author=author,user=current_user,blogLength=blogLength)

@views.route("/profile")
def userPage():
    return render_template("profile.html",user=current_user)

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