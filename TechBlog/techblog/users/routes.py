# All imports

import os
from flask import (render_template, url_for, flash,
                   redirect, request, Blueprint, current_app)
from flask_login import login_user, current_user, logout_user, login_required
from techblog import db, bcrypt
from techblog.models import User, Post
from techblog.users.forms import (
    RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm)
from techblog.users.utils import save_picture, send_reset_email

# users is the name of package.
users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    # is_authenticated
    # This property should return True if the user is authenticated, i.e. they have provided valid credentials. (Only authenticated users will fulfill the criteria of login_required.)

    # if user is login already then it can't register. So redirect it back to home
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    # creating instance of RegistrationForm class
    form = RegistrationForm()

    # if form is submitted successfully
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    # if already one of the user is logged in then redirect it to home as there should be only one user logged in at a time.
    if current_user.is_authenticated:   # current_user is built in proxy for logged user. We can access logged in user using current_user
        return redirect(url_for('main.home'))

    form = LoginForm()
    # if the details provided by user satisfy the validation of each field (username, email, password, etc)
    if form.validate_on_submit():
        # it ret
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

# request.args.next returns none if user is trying to move to another page directly from url section
# it is used here if user is not logged in then we need to render it to home page. We can't give him access to the requested url. Here this url is basically  localhost://account.html

# When the log in view is redirected to, it will have a next variable in the query string, which is the page that the user was trying to access.
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('main.home'))

        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required  # built in decorator available in flask which is used to check whether user is logged in or not
# it will work according to the login_view mentioned. It is mentioned as 'login' in __init__.py file
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            if current_user.image_file != 'default.png':
                previous_picture_file = os.path.join(
                    current_app.root_path, 'static/profile_pics/', current_user.image_file
                )
            else:
                previous_picture_file = ''
            current_user.image_file = picture_file
            # deleting previous profile picture
            if previous_picture_file:
                os.remove(previous_picture_file)

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))

    # first time when user come to account route that time request is GET. So set the form data to the user data. So that it will be displayed to the user(as previous data) instead of blank data.
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for(
        'static', filename='profile_pics/'+current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route('/user/<string:username>', methods=['GET', 'POST'])
def user_posts(username):
    page = request.args.get('page', 1, type=int)

    # getting the user object who is the author of post to which current user is trying to access
    user = User.query.filter_by(username=username).first_or_404()

# arranging the all posts of that author according to the posted time of each post.
    posts = Post.query.filter_by(author=user).order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    # if already one of the user is logged in then redirect it to home as there should be only one user logged in at a time.
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset password', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset-Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()
    # if form is submitted successfully
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')

        user.password = hashed_password
        db.session.commit()
        flash('Your Password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset-token', form=form)


# delete account
@login_required
@users.route("/delete_account", methods=['GET', 'POST'])
def delete_account():
    user = current_user._get_current_object()
    posts = Post.query.filter_by(author=user).all()

    for post in posts:
        db.session.delete(post)
        db.session.commit()

    if user.image_file != "default.png":
        user_profile = os.path.join(current_app.root_path, 'static/profile_pics/', user.image_file)
        os.remove(user_profile)

    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('main.home'))
