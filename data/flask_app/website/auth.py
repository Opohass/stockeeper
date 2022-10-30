from operator import and_
from flask import Blueprint, render_template, request, flash, redirect, url_for
import re
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get("password")
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            if check_password_hash(user.password, password):
                flash("Logged In Successfully", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect Password", category="error")
        else:
            flash('Email Does Not Exist', category="error")
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        password_matching_regex = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$"
        print(request.form)
        print(type(email))
        print(email)
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exists", category="error")
        elif ('@' not in email) or (not (email.endswith('.com') or email.endswith('.co.il'))):
            flash("Email must contain an '@' symbol and end with either '.com' or '.co.il'", category='error')
        elif not re.match(password_matching_regex, password1):
            flash("Password Must Contain at least a number, upper-case letter, lower-case letter and be at least 8 characters long", category="error")
        elif password1 != password2:
            flash("Password and Confirmation must match", category="error")
        else:
            new_user = User(email=email, firstname=firstname, lastname=lastname, password=generate_password_hash(password1, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            user = User.query.filter_by(email=email).first()
            login_user(user, remember=True)
            flash("Account Created Successfully!", category="success")
            return redirect(url_for("views.manage"))
            
    return render_template("signup.html", user=current_user)
