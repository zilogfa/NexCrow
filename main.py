"""
Crow Nexus - Social Media Platform
started on: July/08/2023
"""

from flask import Flask, render_template, url_for, redirect, jsonify, flash, request
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
from PIL import Image  # pip Pillow
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

    likes = db.Table('likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)

    followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)
    

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
        comments = db.relationship('Comment', back_populates='user')
        liked_posts = db.relationship('Post', secondary=likes, backref='likers')

        followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
    )
        
        def follow(self, user):
            if not self.is_following(user):
                self.followed.append(user)

        def unfollow(self, user):
            if self.is_following(user):
                self.followed.remove(user)

        def is_following(self, user):
            return self.followed.filter(followers.c.followed_id == user.id).count() > 0


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
        comments = db.relationship('Comment', back_populates='post')
        

    class Comment(db.Model):
        __tablename__ = 'comments'
        id = db.Column(db.Integer, primary_key=True)
        content = db.Column(db.String(255), nullable=False)
        timestamp = db.Column(db.DateTime, nullable=False,
                              default=datetime.utcnow)
        user_id = db.Column(db.Integer, db.ForeignKey(
            'user.id'), nullable=False)
        post_id = db.Column(db.Integer, db.ForeignKey(
            'post.id'), nullable=False)

        user = db.relationship('User', back_populates='comments')
        post = db.relationship('Post', back_populates='comments')

    

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

    class CommentForm(FlaskForm):
        """Comment Form: TextArea - Submit-btn"""
        comment = TextAreaField('Post',
                                validators=[
                                    DataRequired(), Length(min=1, max=280)],
                                render_kw={'class': '',
                                           'placeholder': 'Type Something'}
                                )
        submit = SubmitField('Submit', render_kw={'class': ''})

    # -------------------- Pages  ----------------------------------------------
    # -------------------- Home Page  ------------------------------------------
    # if NOT logged_in: see All posts and Login/Register btn's NavBar
    # if logged_in: see all posts & access more features: Likes, & Edit your own post.

    @app.route('/')
    def home():
        all_posts = Post.query.order_by(Post.created_at.desc()).all() # Sorting and Reversing by created_at time
        return render_template('index.html', posts=all_posts, current_user=current_user, logged_in=current_user.is_authenticated)

    # -------------------- Profile Page  ---------------------------------------
    @app.route('/profile')
    @login_required
    def profile():
        """Current User Profile page - include all posts"""
        user_posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.created_at.desc()).all() #reversing posts based on created_at , and calling posts by user id
        return render_template('profile.html', user_posts=user_posts, current_user=current_user, logged_in=current_user.is_authenticated)

    # -------------------- User Profile Page by ID  -------------------------
    @app.route('/<int:user_id>')
    @login_required
    def user_profile(user_id):
        user = User.query.get(user_id)
        
        if user:
            reversed_posts = Post.query.filter_by(user_id=user.id).order_by(Post.created_at.desc()).all()
            return render_template('user_profile.html', user=user, posts=reversed_posts, current_user=current_user, logged_in=current_user.is_authenticated)
        else:
            flash('User not found.')
            return redirect(url_for('home'))

    # --------------------- Post Page by ID --------------------------------------
    @app.route('/showpost/<int:post_id>', methods=['GET', 'POST'])
    def show_post(post_id):
        requested_post = Post.query.get(post_id)
        form = CommentForm()
        if form.validate_on_submit():
            user_id = current_user.id
            post = Post.query.get(post_id)
            user = User.query.get(user_id)

            new_comment = Comment(content=form.comment.data, user=user, post=post)
            db.session.add(new_comment)
            db.session.commit()
            flash('Comment added successfully.')
            return redirect(url_for('show_post', post_id=post_id))    
        
        if requested_post:
            return render_template('showpost.html', form=form, post=requested_post, current_user=current_user, logged_in=current_user.is_authenticated)
        else:
            flash('Post not found.')
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
    

    # -------------------- Like Function ---------------------------------------
    #---------------------------------------------------------------------------
    #---------------------------------------------------------------------------

    @app.route('/like/<int:post_id>', methods=['POST'])
    @login_required
    def like_post(post_id):
        # Get the current user

        # Get the post
        post = Post.query.get(post_id)
        print("USER CALLED Like_Post function ///////////////////////////")
        if post and current_user:
            if post in current_user.liked_posts:
                # User already liked the post, remove the like
                current_user.liked_posts.remove(post)
                post.likes -= 1
                print("USER Like_Post post.Likes -=1 ///////////////////////////")
            else:
                # User didn't like the post yet, add the like
                current_user.liked_posts.append(post)
                post.likes += 1
                print("USER Like_Post post.Likes +=1 ///////////////////////////")

            db.session.commit()
            flash('Post liked successfully.')
        else:
            flash('Post not found.')

        return redirect(url_for('show_post', post_id=post_id))
    
    # -------------------- Follow / Unfollow -----------------------------------
    #---------------------------------------------------------------------------

    # Follow .................................................
    @app.route('/user/<int:user_id>/follow', methods=['POST'])
    @login_required
    def follow(user_id):
        user = User.query.get(user_id)
        if user:
            current_user.follow(user)
            db.session.commit()
            flash('You are now following {}'.format(user.username))
        else:
            flash('User not found')
        return redirect(url_for('user_profile', user_id=user_id))

    #Unfollow ..................................................
    @app.route('/user/<int:user_id>/unfollow', methods=['POST'])
    @login_required
    def unfollow(user_id):
        user = User.query.get(user_id)
        if user:
            current_user.unfollow(user)
            db.session.commit()
            flash('You have unfollowed {}'.format(user.username))
        else:
            flash('User not found')
        return redirect(url_for('user_profile', user_id=user_id))

    # -------------------- Edit Page  ------------------------------------------

    @app.route('/edit-post/<int:post_id>', methods=['POST', 'GET'])
    @login_required
    def edit_post(post_id):
        post = Post.query.get_or_404(post_id)
        edit_form = PostForm(obj=post)
        if edit_form.validate_on_submit():
            post.body = edit_form.body.data
            db.session.commit()
            return redirect(url_for('profile'))
        return render_template('edit_post.html', form=edit_form ,post=post, current_user=current_user, logged_in=current_user.is_authenticated)

    # -------------------- Delete Page  -----------------------------------------

    @app.route('/delete-post')
    @login_required
    def delete_post():
        id = request.args.get('post_id')
        post_to_delete = Post.query.get(id)
        db.session.delete(post_to_delete)
        db.session.commit()
        return redirect('profile')

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
