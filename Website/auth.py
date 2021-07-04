from flask import Blueprint,redirect,url_for
from flask.templating import render_template
from flask import request,flash
from . import db
from .models import User 

from flask_login import login_user,logout_user,current_user,login_required

from werkzeug.security import generate_password_hash,check_password_hash


auth=Blueprint('auth',__name__)

@auth.route('/login',methods=['GET','POST'])
   
def login():
     if request.method=="POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if user:
           if check_password_hash(user.password,password):
              flash("Logged in successfully",category='success')
              login_user(user,remember=True)
              return redirect(url_for("views.home"))
           else:
              flash("Wrong Password",category='error')
        else:
           flash("User does not exist",category='error')
     return render_template("login.html",user=current_user)

@auth.route('/logout')
@login_required
def logout():
     logout_user()
     return redirect(url_for("auth.login"))
    
@auth.route('/signup',methods=['GET','POST'])
   
def signup():
     if request.method=="POST":
         firstName=request.form.get('firstName')
         lastName=request.form.get('lastName')
         email=request.form.get('email')
         phoneNumber=request.form.get('phoneNumber')
         password1=request.form.get('password1')
         confirmPassword=request.form.get('confirmPassword')
         
         user=User.query.filter_by(email=email).first()
         if user:
            flash("Email already exists",category='error')
         elif len(firstName)<3:
            flash("First Name should be more than 3 characters long",category='error')
         elif len(lastName)<3:
            flash("Last Name should be more than 3 characters long",category='error')
         elif len(phoneNumber)<8:
              flash("Contact number must be of minimum length 8",category='error')
         elif(password1!=confirmPassword):
            flash("The passwords do not match",category='error')
         else:
             newAccount=User(email=email,firstName=firstName,lastName=lastName,phoneNumber=phoneNumber,password=generate_password_hash(password1,'sha256'))
             db.session.add(newAccount)
             db.session.commit()
             login_user(user,remember=True)
             flash("Account was successfully created",category='success')
             return redirect(url_for("views.home"))
     return render_template("signup.html",user=current_user)

@auth.route("/editprofile",methods=['GET','POST'])
@login_required
def editProfile():
      userLoggedIn=current_user
      if request.method=="POST":
         firstName=request.form.get('firstName')
         lastName=request.form.get('lastName')
         email=request.form.get('email')
         phoneNumber=request.form.get('phoneNumber')
         password1=request.form.get('password1')
         confirmPassword=request.form.get('confirmPassword')
         
         user=User.query.filter_by(id=userLoggedIn.id).first()
         if len(firstName)<3:
            flash("First Name should be more than 3 characters long",category='error')
         if len(lastName)<3:
            flash("Last Name should be more than 3 characters long",category='error')
         if len(phoneNumber)<8:
              flash("Contact number must be of minimum length 8",category='error')
         if(password1!=confirmPassword):
            flash("The passwords do not match",category='error')
         else:
             user.firstName=firstName
             user.lastName=lastName
             user.email=email
             user.phoneNumber=phoneNumber
             user.password=generate_password_hash(password1)
             db.session.commit()
             flash("Account was successfully updated",category='success')
             return redirect(url_for("views.home"))
      return render_template("editprofile.html",user=current_user)