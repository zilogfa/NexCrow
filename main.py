"""
Crow Nexus - Social Media Platform
started on: July/08/2023
"""

from flask import Flask, render_template, url_for, redirect, jsonify, flash
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, TelField, TextAreaField, BooleanField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, InputRequired, Length, ValidationError, EqualTo, Email

from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_bcrypt import Bcrypt

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

from datetime import datetime

import os
import secrets
from PIL import Image  # pip pillow
from flask import current_app

# ----------------- Configuring Flask, Bcrypt & Connecting to DB -----------------

app = Flask(__name__)
app.config['SECRET_KEY'] = 'My-Secret-Key'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['UPLOAD_FOLDER'] = 'static/profile_pictures'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


# -------------------- Configuring Auth Req --------------------------------------

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# -------------------- Profile picture Storing function Setup ---------------------

def save_profile_picture(file):
    # Generating a secure random string as the filename
    random_hex = secrets.token_hex(8)
    # Getting the file extension
    _, file_extension = os.path.splitext(file.filename)
    # Creating a new filename using the random string and the original extension
    new_filename = random_hex + file_extension
    # Setting the destination folder to save the profile pictures
    destination = os.path.join(
        current_app.root_path, 'static/profile_pictures', new_filename)

    # Resize=zing the image to a desired size (optional)
    output_size = (400, 400)  # Adjust the size as needed
    image = Image.open(file)
    image.thumbnail(output_size)

    # Saving the resized image to the destination folder
    image.save(destination)

    # Returning the filename to store in the database
    return new_filename


# -------------------- DATABASE Tables  -----------------------------------------
with app.app_context():
    class User(db.Model, UserMixin):
        """User Meta Data DB:--> id(unique), username[String(40)], email[String(80)], phone_number[String(20)], password[String(80)], created_at[datetime.utc], updated_at[datetime.utc], is_blocked[Boolean]"""
        __tablename__ = 'user'
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(40), nullable=False, unique=False)
        email = db.Column(db.String(80), nullable=False, unique=True)
        phone_number = db.Column(db.String(20))
        password = db.Column(db.String(100), nullable=False)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(
            db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        is_blocked = db.Column(db.Boolean, default=False)
        profile_picture = db.Column(db.String(100))

        posts = relationship('Post', back_populates='user')

    class Post(db.Model):
        """Post Meta Data DB: body[Text], likes[default=0], created_at[utcnow], updated_at[utcnow]"""
        __tablename__ = 'post'
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey(
            'user.id'), nullable=False)
        body = db.Column(db.Text, nullable=False)
        likes = db.Column(db.Integer, default=0)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow)

        user = relationship('User', back_populates='posts')

    db.create_all()

    # -------------------- WTForms Setup  -----------------------------------------

    class PostForm(FlaskForm):
        """Post Form: body:Text, Submit:Btn"""
        body = TextAreaField('Post',
                             validators=[
                                 DataRequired(), Length(min=1, max=280)],
                             render_kw={'class': '',
                                        'placeholder': 'Type Something'}
                             )
        submit = SubmitField('Submit', render_kw={'class': ''})

    class RegisterForm(FlaskForm):
        """Registeration Form: username, email, Phone_Number, Password, Submit btn"""
        username = StringField('Name', validators=[
            DataRequired(), Length(min=2, max=20)], render_kw={'placeholder': 'Display Name'})
        email = EmailField('Email', validators=[DataRequired()], render_kw={
                           'placeholder': 'Email'})
        phone_number = TelField('Phone Number', validators=[DataRequired(), Length(min=6, max=20)], render_kw={
                                'placeholder': 'Phone Number'})
        password = PasswordField('Password', validators=[
            DataRequired(), Length(min=6, max=20)], render_kw={'placeholder': 'Password'})
        # Add the profile picture field
        profile_picture = FileField('Profile Picture', validators=[
                                    FileAllowed(['jpg', 'jpeg', 'png'])])

        submit = SubmitField('Register')

        def validate_user_email(self, email):
            """Validating if user already Existed"""
            existing_user_email = User.query.filter_by(
                email=email.data).first()
            if existing_user_email:
                raise ValidationError(
                    "That email already exist. Please choose a diffent one.")

    class LoginForm(FlaskForm):
        """Login Form: email, Password, login-btn"""
        email = EmailField('Email', validators=[DataRequired()], render_kw={
                           'placeholder': 'Email'})
        password = PasswordField('Password', validators=[
            DataRequired(), Length(min=6, max=20)], render_kw={'placeholder': 'Password'})
        submit = SubmitField('Login')

    # -------------------- Pages  ----------------------------------------------
    # -------------------- Home Page  ------------------------------------------
    # if NOT logged_in: see All posts and Login/Register btn's NavBar
    # if logged_in: see all posts & access more features: Likes, & Edit your own post.

    @app.route('/')
    def home():
        all_posts = Post.query.all()
        return render_template('index.html', posts=all_posts, current_user=current_user, logged_in=current_user.is_authenticated)

    # -------------------- Profile Page  ---------------------------------------
    @app.route('/profile')
    @login_required
    def profile():
        all_user_posts = current_user.posts
        return render_template('profile.html', user_posts=all_user_posts, current_user=current_user, logged_in=current_user.is_authenticated)

    # -------------------- Other User Profile Page  -----------------------------
    @app.route('/<int:user_id>')
    def user_posts(user_id):
        user = User.query.get(user_id)
        if user:
            posts = user.posts
            return render_template('user_posts.html', user=user, posts=posts, current_user=current_user, logged_in=current_user.is_authenticated)
        else:
            flash('User not found.')
            return redirect(url_for('home'))

    # -------------------- Create New Post Page  --------------------------------

    @app.route('/post', methods=['POST', 'GET'])
    @login_required
    def new_post():
        form = PostForm()
        if form.validate_on_submit():
            new_post = Post(
                user=current_user,
                body=form.body.data
            )
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('home'))
        return render_template('new_post.html', form=form, logged_in=current_user.is_authenticated)

    # -------------------- Edit Page  ------------------------------------------

    @app.route('/edit-post/<int:post_id>', methods=['POST', 'GET'])
    def edit_post(post_id):
        return render_template('edit.html')

    # -------------------- Delete Page  -----------------------------------------

    @app.route('/delete/<int:post_id>', methods=['POST'])
    def delete(post_id):
        return

    # -------------------- About Page  -----------------------------------------

    @app.route('/about')
    def about():
        return render_template('about.html', logged_in=current_user.is_authenticated)

    # -------------------- Register Page  --------------------------------------

    @app.route('/register', methods=['POST', 'GET'])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            if User.query.filter_by(email=form.email.data).first():
                print(User.query.filter_by(email=form.email.data).first())
                # User already exists
                flash("You've already signed up with that email, log in instead!")
                return redirect(url_for('login'))

            # Save the uploaded file
            if form.profile_picture.data:
                profile_picture_filename = save_profile_picture(
                    form.profile_picture.data)
            else:
                profile_picture_filename = None

            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = User(
                username=form.username.data,
                email=(form.email.data).lower(),
                profile_picture=profile_picture_filename,
                phone_number=form.phone_number.data,
                password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))

        return render_template('register.html', form=form)

    # -------------------- Login Page  -----------------------------------------

    @app.route('/login', methods=['POST', 'GET'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(
                email=(form.email.data).lower()).first()
            # Email doesn't exist
            if not user:
                flash("That username does not exist, please try again.")
                return redirect(url_for('login'))
            if user:
                if bcrypt.check_password_hash(user.password, form.password.data):
                    login_user(user)
                    user.updated_at = datetime.utcnow()
                    db.session.commit()
                    return redirect(url_for('home'))
            return redirect(url_for('home'))
        return render_template('login.html', form=form, logged_in=current_user.is_authenticated)

    # -------------------- Logout Page  ----------------------------------------

    @app.route('/logout', methods=['POST', 'GET'])
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('home'))

    if __name__ == '__main__':
        app.run(debug=True)
