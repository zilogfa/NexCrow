from app import  db
from flask_login import UserMixin
from sqlalchemy.orm import relationship

from datetime import datetime


# post.likes - user.liked_posts
likes = db.Table('likes',
                    db.Column('user_id', db.Integer, db.ForeignKey(
                        'user.id'), primary_key=True),
                    db.Column('post_id', db.Integer, db.ForeignKey(
                        'post.id'), primary_key=True)
                    )

comment_likes = db.Table('comment_likes',
                            db.Column('user_id', db.Integer, db.ForeignKey(
                                'user.id'), primary_key=True),
                            db.Column('comment_id', db.Integer, db.ForeignKey(
                                'comments.id'), primary_key=True)
                            )

# followers = user.followers.all()  # followed = user.followed.all()
followers = db.Table('followers',
                        db.Column('follower_id', db.Integer, db.ForeignKey(
                            'user.id'), primary_key=True),
                        db.Column('followed_id', db.Integer,
                                db.ForeignKey('user.id'), primary_key=True)
                        )

# Block Users
blocked = db.Table('blocked',
                    db.Column('blocker_id', db.Integer, db.ForeignKey(
                        'user.id'), primary_key=True),
                    db.Column('blocked_id', db.Integer, db.ForeignKey(
                        'user.id'), primary_key=True)
                    )

# Mute Users
muted = db.Table('muted',
                    db.Column('muter_id', db.Integer, db.ForeignKey(
                        'user.id'), primary_key=True),
                    db.Column('muted_id', db.Integer, db.ForeignKey(
                        'user.id'), primary_key=True)
                    )

class User(db.Model, UserMixin):
    """User Meta Data DB:--> id(unique), username[String(40)], email[String(80)], phone_number[String(20)], password[String(80)], created_at[datetime.utc], updated_at[datetime.utc], is_blocked[Boolean]"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(11), unique=True, nullable=False)

    username = db.Column(db.String(40), nullable=False, unique=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    profile_picture = db.Column(db.String(80))
    header_picture = db.Column(db.String(80))
    bio = db.Column(db.Text, nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    location = db.Column(db.String(30), nullable=True)
    birthday = db.Column(db.DateTime, nullable=True)
    bio_url = db.Column(db.String(255), nullable=True)
    profile_impressions = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_blocked = db.Column(db.Boolean, default=False)
    is_private = db.Column(db.Boolean, default=False)
    dark_theme = db.Column(db.Boolean, default=False)

    # relations
    posts = relationship('Post', back_populates='user')
    comments = db.relationship('Comment', back_populates='user')
    liked_posts = db.relationship(
        'Post', secondary=likes, backref='likers')
    liked_comments = db.relationship(
        'Comment', secondary=comment_likes, backref='likers')
    blocked_users = db.relationship('User', secondary=blocked,
                                    primaryjoin=(
                                        blocked.c.blocker_id == id),
                                    secondaryjoin=(
                                        blocked.c.blocked_id == id),
                                    backref=db.backref(
                                        'blocking_users', lazy='dynamic'),
                                    lazy='dynamic')

    muted_users = db.relationship('User', secondary=muted,
                                    primaryjoin=(muted.c.muter_id == id),
                                    secondaryjoin=(muted.c.muted_id == id),
                                    backref=db.backref(
                                        'muting_users', lazy='dynamic'),
                                    lazy='dynamic')
    followed = db.relationship('User', secondary=followers,
                                primaryjoin=(followers.c.follower_id == id),
                                secondaryjoin=(
                                    followers.c.followed_id == id),
                                backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    # def followed_posts(self):
    #     # Get the IDs of followed users
    #     followed_ids = [user.id for user in self.followed]

    #     # Include your own user ID
    #     followed_ids.append(self.id)

    #     # Query all posts from users in the followed_ids list
    #     return Post.query.filter(Post.user_id.in_(followed_ids)).order_by(desc(Post.created_at)).all()

    def followed_posts(self):
        # Get the IDs of followed users
        followed_ids = [user.id for user in self.followed]

        # Include your own user ID
        followed_ids.append(self.id)

        # Query all posts from users in the followed_ids list
        return Post.query.filter(Post.user_id.in_(followed_ids))

    # -------- block and Mute Funcs:
    def block(self, user):
        if not self.is_blocking(user):
            self.blocked_users.append(user)

    def unblock(self, user):
        if self.is_blocking(user):
            self.blocked_users.remove(user)

    def is_blocking(self, user):
        return self.blocked_users.filter(blocked.c.blocked_id == user.id).count() > 0

    def mute(self, user):
        if not self.is_muting(user):
            self.muted_users.append(user)

    def unmute(self, user):
        if self.is_muting(user):
            self.muted_users.remove(user)

    def is_muting(self, user):
        return self.muted_users.filter(muted.c.muted_id == user.id).count() > 0

class Post(db.Model):  # user.posts.all()
    """Post Meta Data DB: body[Text], likes[default=0], created_at[utcnow], updated_at[utcnow]"""
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)
    body = db.Column(db.Text, nullable=False)
    post_picture = db.Column(db.String(200))
    likes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    post_impressions = db.Column(db.Integer, default=0)

    user = relationship('User', back_populates='posts')
    comments = db.relationship(
        'Comment', back_populates='post', cascade="all, delete-orphan")
    media = db.relationship(
        'Media', back_populates='post', uselist=True, cascade="all, delete-orphan")

    # def process_post_body(self):
    #     # Convert URLs into clickable links
    #     self.body = re.sub(
    #         r'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)',
    #         r'<a href="\1" target="_blank">\1</a>', self.body)

    #     # Convert hashtags into clickable search links
    #     self.body = re.sub(
    #         r'#(\w+)', r'<a href="/search/\1">#\1</a>', self.body)

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id'), nullable=False)
    media_type = db.Column(db.Enum('image', 'video'), nullable=False)
    media_url = db.Column(db.String(200), nullable=False)
    media_order = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    post = db.relationship('Post', back_populates='media')

class Comment(db.Model):  # user.comments.all()
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    comment_impressions = db.Column(db.Integer, default=0)
    likes_count = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id'), nullable=False)

    user = db.relationship('User', back_populates='comments')
    post = db.relationship('Post', back_populates='comments')
    parent_comment_id = db.Column(
        db.Integer, db.ForeignKey('comments.id'), nullable=True)
    replies = db.relationship('Comment', backref=db.backref(
        'parent', remote_side=[id]), lazy='dynamic')

    # def process_comment_content(self):
    #     # Convert URLs into clickable links
    #     self.content = re.sub(
    #         r'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)',
    #         r'<a href="\1" target="_blank">\1</a>', self.content)

    #     # Convert hashtags into clickable search links
    #     self.content = re.sub(
    #         r'#(\w+)', r'<a href="/search/\1">#\1</a>', self.content)

class UserLoginHistory(db.Model):  # user.login_history.all()
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    # Storing IP addresses as strings
    ip_address = db.Column(db.String(45))

    # Defining a relationship to the User model
    user = db.relationship('User', backref=db.backref(
        'login_history', lazy='dynamic'))

    def __init__(self, user_id, ip_address):
        self.user_id = user_id
        self.ip_address = ip_address

    def save(self):
        db.session.add(self)
        db.session.commit()