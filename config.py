import os

DATABASE_URL = ""

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', "8BYkEfBA6O6donzWlSihBXox7C0sKR6b")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL",  "sqlite:///site.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    UPLOAD_FOLDER = 'static'