import os
import secrets
from PIL import Image
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import app, db, mail
from app.models import User
from app.users.forms import LoginForm, RegisterForm, UpdateForm, ResetRequestForm, PasswordResetForm
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

users_blueprint = Blueprint('users', __name__, template_folder='templates/users')

@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are logged out!', 'warning')
    return redirect(url_for('index'))

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user, remember=form.remember.data)
            flash('Login Successfull!', 'success')
            next = request.args.get('next')
            if next == None or not next[0] == '/' or next == '/logout':
                next = url_for('index')
            return redirect(next)
        else:
            flash('Password is incorrect. Please retry.', 'danger')

    return render_template('login.html', form=form, title='Login')

@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterForm()

    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        user = User(email, username, password)

        db.session.add(user)
        db.session.commit()

        flash('Your account has been successfully created!', 'success')
        return redirect(url_for('users.login'))

    return render_template('register.html', form=form, title='Register')

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img', picture_fn)
    # form_picture.save(picture_path)

    output_size = (200, 200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@users_blueprint.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Account detail updated.", "success")
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='img/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password, click on the below link:
    {url_for('users.reset_token', token=token, _external=True)}

    If you did not make this request, simply ignore this mail.
    '''
    mail.send(msg)

@users_blueprint.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset.html', title='Reset Password', form=form)

@users_blueprint.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token.', 'warning')
        return redirect(url_for('users.reset_password'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated.', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_password.html', title='Reset Password', form=form)
