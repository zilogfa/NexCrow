"""
Crow Nexus - Social Media Platform
started on: July/08/2023
"""


from flask import Flask
from flask import Blueprint
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


# ----------------- Configuring Flask, DB, Bcrypt, Upload folder  ----

app = Flask(__name__)
from config import Config
from app.forms import *

csrf = CSRFProtect(app)
app.config.from_object(Config)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'mp4', 'avi', 'mov'}
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)



#Auth login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# DB
from .models.user import *
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# all routes
from app.routes import *