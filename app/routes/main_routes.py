from app import app, db, bcrypt
from app.models.user import *
from app.forms import *

from flask import render_template, url_for, redirect, jsonify, flash, request, make_response, g
from flask_wtf.csrf import generate_csrf

from werkzeug.utils import secure_filename
from flask_login import login_user, login_required, current_user, logout_user
from sqlalchemy import desc
from sqlalchemy import func

from datetime import datetime
import random

import re  # for identifying and converting # & URL in user posts to <a>

import os
import secrets
from PIL import Image  # pip Pillow
from flask import current_app



# -------- Globally to all render_templates ---------------------------------------
@app.before_request
def before_request():
    """universally accessible without repeatedly passing them manually to every render_template call."""
    g.csrf_token = generate_csrf()  # from flask import g


# -------------------- Generating Unique ID -----------------------------------------
def generate_unique_id():
    """ Unique 11-Digit ID for each user oppon registeration """
    while True:
        # generate a random 11-digit number
        unique_id = str(random.randint(10000000000, 99999999999))
        user_with_id = User.query.filter_by(unique_id=unique_id).first()
        if not user_with_id:
            return unique_id
# -------------------- Converting Posts # & URL to clickable <a>  -------------------


def process_post_body(body):
    # Convert URLs into clickable links
    body = re.sub(
        r'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)',
        r'<a href="\1" target="_blank" class="url-link">\1</a>', body
    )

    # Convert hashtags into clickable search links
    body = re.sub(
        r'#(\w+)', r'<a href="/search?query=\1" class="hashtag-link">#\1</a>', body)

    return body

# -------------------- if an uploaded file has a valid extension ------------------


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# -------------------- Profile picture Storing function Setup ---------------------


def save_profile_picture(file):
    if not file:
        return None
    # Generating a secure random string as the filename
    random_hex = secrets.token_hex(8)
    # Getting the file extension
    _, file_extension = os.path.splitext(file.filename)
    # Creating a new filename using the random string and the original extension
    new_filename = random_hex + file_extension
    # Setting the destination folder to save the post pictures
    destination = os.path.join(
        current_app.root_path, 'static/profile_pictures', new_filename)

    # Resize the image to a desired size (optional)
    output_size = (800, 800)  # Adjust the size as needed
    image = Image.open(file)
    width, height = image.size
    size = min(width, height)
    left = (width - size) / 2
    top = (height - size) / 2
    right = (width + size) / 2
    bottom = (height + size) / 2
    image = image.crop((left, top, right, bottom))
    image.thumbnail(output_size)

    # Saving the resized image to the destination folder
    image.save(destination)

    # Returning the filename to store in the database
    return new_filename


# -------------------- Post picture Storing Setup ---------------------

def save_post_picture(file):
    if not file:
        return None
    # Generating a secure random string as the filename
    random_hex = secrets.token_hex(8)
    # Getting the file extension
    _, file_extension = os.path.splitext(file.filename)
    # Creating a new filename using the random string and the original extension
    new_filename = random_hex + file_extension
    # Setting the destination folder to save the post pictures
    destination = os.path.join(
        current_app.root_path, 'static/post_pictures', new_filename)

    # Resize the image to a desired size (optional)
    output_size = (1200, 1200)  # Adjust the size as needed
    image = Image.open(file)
    image.thumbnail(output_size)

    # Saving the resized image to the destination folder
    image.save(destination)

    # Returning the filename to store in the database
    return new_filename


# -------------------- Header picture Storing Setup ---------------------

def save_header_picture(file):
    if not file:
        return None
    # Generating a secure random string as the filename
    random_hex = secrets.token_hex(8)
    # Getting the file extension
    _, file_extension = os.path.splitext(file.filename)
    # Creating a new filename using the random string and the original extension
    new_filename = random_hex + file_extension
    # Setting the destination folder to save the post pictures
    destination = os.path.join(
        current_app.root_path, 'static/header_pictures', new_filename)

    # Resize the image to a desired size (optional)
    output_size = (1000, 1000)  # Adjust the size as needed
    image = Image.open(file)
    image.thumbnail(output_size)

    # Saving the resized image to the destination folder
    image.save(destination)

    # Returning the filename to store in the database
    return new_filename


# -------------------- DATABASE Tables  -----------------------------------------




# -------------------- WTForms Setup  -----------------------------------------



# -------------------- Pages  ----------------------------------------------
# -------------------- Home Page  ------------------------------------------
# if NOT logged_in: see All posts and Login/Register
# if logged_in: see all posts & access more features: Post, Likes, & Delete & Edit your own post.

@app.route('/')
def all():
    # Sorting and Reversing by created_at time
    all_posts = Post.query.order_by(Post.created_at.desc()).all()
    for post in all_posts:
        post.body = process_post_body(post.body)
    return render_template('index.html', posts=all_posts, current_user=current_user, logged_in=current_user.is_authenticated)

# -------------------- Home Page  ------------------------------------------
# if NOT logged_in: see All posts and Login/Register
# if logged_in: see all posts & access more features: Post, Likes, & Delete & Edit your own post.

@app.route('/home')
@login_required
def home_page():
    followed_posts = current_user.followed_posts().order_by(
        Post.created_at.desc()).all()
    for post in followed_posts:
        post.body = process_post_body(post.body)
    return render_template('home.html', posts=followed_posts, current_user=current_user, logged_in=current_user.is_authenticated)

@app.route('/home_v2')
@login_required
def home_page_v2():
    return render_template('home_v2.html', current_user=current_user, logged_in=current_user.is_authenticated)

# API HOME

# @app.route('/api/home_posts', methods=['GET'])
# @login_required
# def api_home_posts():
#     followed_posts = current_user.followed_posts()
#     posts_data = []

#     for post in followed_posts:
#         post_data = {
#             'post_id': post.id,
#             'user_id': post.user.id,
#             'username': post.user.username,
#             'unique_id': post.user.unique_id,
#             'post_picture': post.post_picture,

#             'post_body': process_post_body(post.body),
#             'profile_picture': post.user.profile_picture or url_for('static', filename='images/blank-profile-pic.png'),

#             'likes': post.likes,
#             'comments_count': len(post.comments),
#             'post_impressions': post.post_impressions,
#             'created_at': post.created_at.strftime('%H:%M · %B %d, %Y')
#         }
#         posts_data.append(post_data)

#     return jsonify(posts_data)

# API HOME 2

@app.route('/api/home_posts', methods=['GET'])
@login_required
def api_home_posts():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    followed_posts_query = current_user.followed_posts().order_by(desc(Post.created_at))
    followed_posts_pagination = followed_posts_query.paginate(
        page=page, per_page=limit, error_out=False)

    followed_posts = followed_posts_pagination.items
    next_url = url_for('api_home_posts', page=followed_posts_pagination.next_num, limit=limit) \
        if followed_posts_pagination.has_next else None

    posts_data = []

    for post in followed_posts:
        post_data = {
            'post_id': post.id,
            'user_id': post.user.id,
            'username': post.user.username,
            'unique_id': post.user.unique_id,
            'post_picture': post.post_picture,

            'post_body': process_post_body(post.body),
            'profile_picture': post.user.profile_picture or url_for('static', filename='images/blank-profile-pic.png'),

            'likes': post.likes,
            'comments_count': len(post.comments),
            'post_impressions': post.post_impressions,
            'created_at': post.created_at.strftime('%H:%M · %B %d, %Y')
        }
        posts_data.append(post_data)

    return jsonify({
        'posts': posts_data,
        'next_url': next_url,
        'moreAvailable': followed_posts_pagination.has_next
    })

# -------------------- User Statistics  ------------------------------------------
@app.route('/user_stats/')
@login_required
def user_stats():
    user = current_user

    # Received Likes comments & Posts if any
    rec_posts_likes = 0
    if db.session.query(
            func.sum(Post.likes)).filter_by(user_id=user.id).scalar():
        rec_posts_likes = db.session.query(
            func.sum(Post.likes)).filter_by(user_id=user.id).scalar()

    rec_comments_likes = 0
    if db.session.query(
            func.sum(Comment.likes_count)).filter_by(user_id=user.id).scalar():
        rec_comments_likes = db.session.query(
            func.sum(Comment.likes_count)).filter_by(user_id=user.id).scalar()

    # passing values
    unique_id = user.unique_id
    total_posts = Post.query.filter_by(user_id=user.id).count()
    total_comments = Comment.query.filter_by(user_id=user.id).count()
    profile_page_impressions = user.profile_impressions
    total_post_impressions = db.session.query(
        func.sum(Post.post_impressions)).filter_by(user_id=user.id).scalar()
    total_comment_impressions = db.session.query(
        func.sum(Comment.comment_impressions)).filter_by(user_id=user.id).scalar()
    most_post_impressions = db.session.query(
        func.max(Post.post_impressions)).filter_by(user_id=user.id).scalar()
    most_comment_impressions = db.session.query(
        func.max(Comment.comment_impressions)).filter_by(user_id=user.id).scalar()
    total_received_likes = rec_posts_likes + rec_comments_likes
    most_received_likes = db.session.query(
        func.max(Post.likes)).filter_by(user_id=user.id).scalar()
    total_given_likes = db.session.query(
        func.count(likes.c.post_id)
    ).filter(likes.c.user_id == user.id).scalar()

    print(
        f"*** static data fetched --- User ID: {user.id} / Email: {user.email} **")
    return jsonify({
        'unique_id': f'@{unique_id}',
        'total_posts': total_posts or 0,
        'total_comments': total_comments or 0,
        'profile_page_impressions': profile_page_impressions or 0,
        'total_post_impressions': total_post_impressions or 0,
        'total_comment_impressions': total_comment_impressions or 0,
        'most_post_impressions': most_post_impressions or 0,
        'most_comment_impressions': most_comment_impressions or 0,
        'total_received_likes': total_received_likes or 0,
        'most_received_likes': most_received_likes or 0,
        'total_given_likes': total_given_likes or 0,
    })

# -------------------- User Profile Page by ID  -------------------------
@app.route('/user_profile/<int:user_id>')
@login_required
def user_profile(user_id):
    user = User.query.get(user_id)

    if user:
        followers = user.followers.all()
        followed = user.followed.all()
        reversed_posts = Post.query.filter_by(
            user_id=user.id).order_by(Post.created_at.desc()).all()
        for post in reversed_posts:
            post.body = process_post_body(post.body)
        return render_template('user_profile.html', user=user, followers=followers, followed=followed, posts=reversed_posts, current_user=current_user, logged_in=current_user.is_authenticated, csrf_token=generate_csrf())
    else:
        flash('User not found.')
        return redirect(url_for('home_page'))
    
#--------------------- followers / following PAGE----------------------------------
@app.route('/followers/<int:user_id>')
@login_required
def user_followers(user_id):
    user = User.query.get(user_id)
    if user:
        followers = user.followers.all()
        return render_template('followers.html', followers=followers, user=user, current_user=current_user,logged_in=current_user.is_authenticated)  
    return redirect(url_for('home_page'))

@app.route('/following/<int:user_id>')
@login_required
def user_following(user_id):
    user = User.query.get(user_id)
    if user:
        following = user.followed.all()
        return render_template('following.html', following=following, user=user, current_user=current_user,logged_in=current_user.is_authenticated)       
    return redirect(url_for('home_page'))
# --------------------- Post Page by ID --------------------------------------
@app.route('/show_post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    requested_post = Post.query.get(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        user_id = current_user.id
        post = Post.query.get(post_id)
        user = User.query.get(user_id)

        new_comment = Comment(
            content=form.comment.data, user=user, post=post)
        db.session.add(new_comment)
        db.session.commit()
        print(f'Comment added successfully. post ID: {post_id}')
        return redirect(url_for('show_post', post_id=post_id))

    if requested_post:
        comments = requested_post.comments
        requested_post.body = process_post_body(requested_post.body)

        if comments:
            for comment in comments:
                comment.content = process_post_body(comment.content)

        return render_template('showpost.html', form=form, post=requested_post, comments=comments, current_user=current_user, logged_in=current_user.is_authenticated)
    else:
        print(f'Post not found. {post_id}')
        return redirect(url_for('home_page'))

# -------------------- Create New Post Page  --------------------------------

@app.route('/post', methods=['POST', 'GET'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if request.files['post_picture']:
            new_post = Post(
                user=current_user,
                body=form.body.data,
                post_picture=save_post_picture(form.post_picture.data)
            )
        else:
            new_post = Post(
                user=current_user,
                body=form.body.data
            )

        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('home_page'))
    return render_template('new_post.html', form=form, logged_in=current_user.is_authenticated)

# -------------------- Edit Post Page  ------------------------------------------

@app.route('/edit-post/<int:post_id>', methods=['POST', 'GET'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    edit_form = PostForm(obj=post)
    if edit_form.validate_on_submit():
        post.body = edit_form.body.data
        if request.files['post_picture']:
            post.post_picture = save_post_picture(
                edit_form.post_picture.data)
        db.session.commit()
        return redirect(url_for('user_profile', user_id=current_user.id))
    return render_template('edit_post.html', form=edit_form, post=post, current_user=current_user, logged_in=current_user.is_authenticated)

# -------------------- Setting Page  -----------------------------------------

@app.route('/setting/', methods=['POST', 'GET'])
@login_required
def setting():
    user = User.query.get_or_404(current_user.id)
    setting = EditRegister(obj=user)
    if setting.validate_on_submit():
        print("////\n\n\n******* SAVE CLICKED \n\n\n\n////////////")
        user.username = setting.username.data
        user.email = setting.email.data
        if request.files['profile_picture']:
            user.profile_picture = save_profile_picture(
                setting.profile_picture.data)
        if request.files['header_picture']:
            user.header_picture = save_header_picture(
                setting.header_picture.data)
        user.bio = setting.bio.data
        user.location = setting.location.data
        user.url = setting.url.data
        if request.files['birthday']:
            user.birthday = setting.birthday.data
        db.session.commit()

        return redirect(url_for('setting'))
    return render_template('setting.html', form=setting, user=user, logged_in=current_user.is_authenticated)

# --- edit profile.................................

@app.route('/edit_profile', methods=['POST', 'GET'])
@login_required
def edit_profile():
    user = User.query.get_or_404(current_user.id)
    form = EditProfile(request.form, obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.bio = form.bio.data
        user.location = form.location.data
        user.birthday = form.birthday.data
        db.session.commit()
        return redirect(url_for('user_profile', user_id=current_user.id))

    response = make_response(render_template('edit_profile.html', form=form, user=user,
                                logged_in=current_user.is_authenticated, current_user=current_user))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

    # --- edit Birthday.................................
@app.route('/edit_birthday', methods=['POST', 'GET'])
@login_required
def edit_birthday():
    user = User.query.get_or_404(current_user.id)
    form = EditBirthday(request.form, obj=user)
    if form.validate_on_submit():
        user.birthday = form.birthday.data
        db.session.commit()
        return redirect(url_for('edit_birthday'))

    response = make_response(render_template('edit_birthday.html', form=form, user=user,
                                logged_in=current_user.is_authenticated, current_user=current_user))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

# --- Edit Profile Pic.................................
@app.route('/edit_profile_pic', methods=['POST', 'GET'])
@login_required
def edit_profile_pic():
    user = User.query.get_or_404(current_user.id)
    form = EditProfilePic()
    if form.validate_on_submit():
        if request.files['profile_picture']:
            # Save the new profile picture and update the user's profile_picture field
            new_profile_picture = save_profile_picture(
                form.profile_picture.data)
            user.profile_picture = new_profile_picture
            db.session.commit()

        return redirect(url_for('edit_profile_pic'))
    return render_template('edit_profile_pic.html', form=form, user=user, logged_in=current_user.is_authenticated, current_user=current_user)

# --- Edit Website URL.................................
@app.route('/edit_website_url', methods=['POST', 'GET'])
@login_required
def edit_website_url():
    user = User.query.get_or_404(current_user.id)
    form = EditURL(obj=user)
    if form.validate_on_submit():
        user.bio_url = form.url.data
        db.session.commit()

        return redirect(url_for('edit_website_url'))
    return render_template('edit_website_url.html', form=form, user=user, logged_in=current_user.is_authenticated, current_user=current_user)

# --- Edit Header Pic.................................
@app.route('/edit_header_pic', methods=['POST', 'GET'])
@login_required
def edit_header_pic():
    user = User.query.get_or_404(current_user.id)
    form = EditHeaderPic()
    if form.validate_on_submit():
        if request.files['header_picture']:
            user.header_picture = save_header_picture(
                form.header_picture.data)
            db.session.commit()

        return redirect(url_for('edit_header_pic'))
    return render_template('edit_header_pic.html', form=form, user=user, logged_in=current_user.is_authenticated, current_user=current_user)
# -------------------- Like Function ---------------------------------------
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

@app.route('/like/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get(post_id)
    if post and current_user:
        if post in current_user.liked_posts:
            current_user.liked_posts.remove(post)
            post.likes -= 1
            liked = False  # to indicate that the post was unliked
        else:
            current_user.liked_posts.append(post)
            post.likes += 1
            liked = True  # to indicate that the post was liked

        db.session.commit()

        # Return the new state and updated like count
        return jsonify({'liked': liked, 'likes': post.likes})

    else:
        return jsonify({'error': 'Post not found.'}), 404

# -------------------- Follow / Unfollow -----------------------------------
# ---------------------------------------------------------------------------

@app.route('/user/<int:user_id>/toggle_follow', methods=['POST'])
@login_required
def toggle_follow(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found!'}), 404

    if current_user.is_following(user):
        current_user.unfollow(user)
        action = 'unfollowed'
    else:
        current_user.follow(user)
        action = 'followed'

    db.session.commit()
    followers_count = user.followers.count()

    return jsonify({'followers_count': followers_count, 'action': action})

# -------------------- Delete Page  -----------------------------------------

@app.route('/delete-post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post:
        if post.user_id == current_user.id:
            db.session.delete(post)
            db.session.commit()
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'Unauthorized access'}), 403
    else:
        return jsonify({'status': 'error', 'message': 'Post not found'}), 404


@app.route('/delete-comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if comment:
        if comment.user_id == current_user.id:
            db.session.delete(comment)
            db.session.commit()
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'Unauthorized access'}), 403
    else:
        return jsonify({'status': 'error', 'message': 'Comment not found'}), 404


# -------------------- About Page  -----------------------------------------

@app.route('/about')
def about():
    return render_template('about.html', logged_in=current_user.is_authenticated, current_user=current_user)

# -------------------- About Page  -----------------------------------------

@app.route('/alert')
def alert():
    return render_template('alert.html', logged_in=current_user.is_authenticated, current_user=current_user)

# -------------------- Impressions for Post/Comment/Profile   ----------------

@app.route('/track_impression/<int:post_id>', methods=['POST'])
def track_impression(post_id):
    # Retrieve the post from the database and update the impression count
    print("Entered the track_impression route")
    post = Post.query.get(post_id)
    if post:
        print(f"Post impressions +1 successfully for post {post.id}")
        post.post_impressions += 1
        db.session.commit()

    return jsonify({'message': 'Impression tracked successfully'})

@app.route('/track_comment_impression/<int:comment_id>', methods=['POST'])
def track_comment_impression(comment_id):
    comment = Comment.query.get(comment_id)
    if comment:
        print(
            f"Comment impressions +1 successfully for comment {comment.id}")
        comment.comment_impressions += 1
        db.session.commit()

    return jsonify({'message': 'Comment Impression tracked successfully'})

@app.route('/track_profile_impression/<int:user_id>', methods=['POST'])
def track_profile_impression(user_id):
    user = User.query.get(user_id)
    if user:
        print(f"Profile impressions +1 successfully for user {user.id}")
        user.profile_impressions += 1
        db.session.commit()

    return jsonify({'message': 'Profile Impression tracked successfully'})

# -------------------- Search  ---------------------------
@app.route('/search')
def search():
    # Get the search term from the query parameter
    query = request.args.get('query')
    if not query:
        flash("Please enter a search query.")
        return redirect(url_for('home_page'))

    # Search for posts/users
    posts = Post.query.filter(Post.body.ilike(f"%{query}%")).all()
    users = User.query.filter(User.username.ilike(f"%{query}%")).all()

    for post in posts:
        post.body = process_post_body(post.body)

    return render_template('search_results.html', posts=posts, users=users, current_user=current_user, logged_in=current_user.is_authenticated, query=query)

# -------------------- Register Page  --------------------------------------

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            print(User.query.filter_by(email=form.email.data).first())
            # User already exists
            flash(
                f"This email address '{form.email.data}' has already been registered!")
            return redirect(url_for('register'))

        # Save the uploaded file
        if form.password.data != form.confirm_password.data:
            # error message using Flask's flash
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))
        if form.profile_picture.data:
            profile_picture_filename = save_profile_picture(
                form.profile_picture.data)
        else:
            profile_picture_filename = None

        hashed_password = bcrypt.generate_password_hash(form.password.data)
        unique_id = generate_unique_id()
        new_user = User(
            username=form.username.data,
            email=(form.email.data).lower(),
            profile_picture=profile_picture_filename,
            unique_id=unique_id,
            password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        print(
            f"### New User: {form.username.data} ,Email: {(form.email.data).lower()}, Unique ID: {unique_id} registered")
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
                return redirect(url_for('all'))
        return redirect(url_for('home_page'))
    return render_template('login.html', form=form, logged_in=current_user.is_authenticated)

# -------------------- Logout Page  ----------------------------------------

@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_page'))

# ----------------------- Refrence for upload -------------------------------

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Save the file URL to the Media model
        media = Media(media_url=filename, media_type='image' if filename.rsplit(
            '.', 1)[1].lower() in ['png', 'jpg', 'jpeg', 'gif', 'webp'] else 'video')
        db.session.add(media)
        db.session.commit()
        return redirect(url_for('index'))

