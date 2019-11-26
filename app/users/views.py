from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import User
from app.users.forms import LoginForm, RegisterForm
from flask_login import login_user, login_required, logout_user, current_user

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
