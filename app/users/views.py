from flask import Blueprint, render_template, redirect, url_for, flash
from app import db
from app.models import User
from app.users.forms import LoginForm, RegisterForm

users_blueprint = Blueprint('users', __name__, template_folder='templates/users')

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        return redirect(url_for('index'))

    return render_template('login.html', form=form, title='Login')

@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
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
