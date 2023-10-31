import os

DATABASE_URL = "postgres://kcmscmvhnpwiyh:49c40b0c048df0c2cb4061e4f2d91af41dffc649b0bc80534259efa67b197a02@ec2-3-212-70-5.compute-1.amazonaws.com:5432/d3p97qn7vo7m2"

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', "49c40b0c048df0c2cb4061e4f2d91af41dffc649b0bc80534259efa67b197a02")
    SQLALCHEMY_DATABASE_URI = os.environ.get(DATABASE_URL,  "sqlite:///site.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    UPLOAD_FOLDER = 'static'