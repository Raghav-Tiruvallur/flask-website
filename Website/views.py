from flask import Blueprint,render_template,request,flash,jsonify,json
from flask_login import login_user,current_user,login_required
views=Blueprint('views',__name__)
from . import db
from .models import Blog

@views.route("/",methods=["GET","POST"])
@login_required
def home():
    blogLength=len(current_user.blogs)
    if request.method=="POST":
        blog=request.form.get('blog')
        if len(blog)<=1:
            flash("Write a longer note !",category='error')
        else:
            newBlogger=Blog(data=blog,userId=current_user.id)
            db.session.add(newBlogger)
            db.session.commit()
            blogLength=len(current_user.blogs)
            flash("Blog added!!",category='success')
    return render_template("home.html",user=current_user,length=blogLength)

@views.route("/delete-Blog",methods=["POST"])

def delete_Blog():
    blog=json.loads(request.data)
    blogID=blog['blogID']
    blog=Blog.query.get(blogID)
    if blog:
        if blog.userId==current_user.userId:
            db.session.delete(blog)
            db.session.commit()
    return jsonify({})


@views.route("/profile")
def userPage():
    return render_template("profile.html",user=current_user)
