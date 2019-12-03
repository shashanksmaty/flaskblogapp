import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

login_manager = LoginManager()

app = Flask(__name__)

# Secret Key setup
app.config['SECRET_KEY'] = '47e396467ad9196c2881c1189a6a396a'

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/flaskblog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create Database instance
db = SQLAlchemy(app)
Migrate(app, db)

login_manager.init_app(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_POST'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_CRED')
mail = Mail(app)

# Import Blueprints
from app.users.views import users_blueprint
from app.blog.views import blog_blueprint
from app.errors.views import error_blueprint

app.register_blueprint(users_blueprint, url_prefix='/')
app.register_blueprint(blog_blueprint, url_prefix='/blog')
app.register_blueprint(error_blueprint)
