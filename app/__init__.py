from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Secret Key setup
app.config['SECRET_KEY'] = '47e396467ad9196c2881c1189a6a396a'

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/flaskblog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create Database instance
db = SQLAlchemy(app)
Migrate(app, db)

# Import Blueprints
from app.users.views import users_blueprint

app.register_blueprint(users_blueprint, url_prefix='/')
