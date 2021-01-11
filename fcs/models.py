# importing the required modules
from datetime import datetime
from fcs import db, login_manager, bcrypt
from flask_login import UserMixin
# importing the required modules end


# defining variable
about = "Uh Oh! Apparently, this user prefers to keep an air of mystery around them. You could check out their stories if you don't mind 😇"
# defining variables end


# loading user using flask_login manager for session management
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# defining the association table for the followers model
followers = db.Table('followers',
                     db.Column('follower_id', db.Integer,
                               db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer,
                               db.ForeignKey('user.id'))
                     )
# defining the association table for the followers model end


# defining the User class (Model)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    profile_pic = db.Column(
        db.String(20), nullable=False, default='profile.png')
    profile_bg = db.Column(
        db.String(20), nullable=False)
    likes_count = db.Column(db.Integer, nullable=False, default=0)
    about = db.Column(db.String(130), nullable=False, default=about)
    stories = db.relationship('Story', backref='author', lazy=True)
    liked = db.relationship(
        'Storylikes',
        foreign_keys='Storylikes.user_id',
        backref='user', lazy='dynamic')
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    # defining unit testing functions
    def set_password(self, password):
        return bcrypt.generate_password_hash(
            password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    # defining unit testing functions end

    def get_followers(self):
        return self.followers.all()

    def get_following(self):
        return self.followed.all()

    # method to like and unlike stories and check if user has liked a story
    def like_story(self, story):
        if not self.has_liked_story(story):
            like = Storylikes(user_id=self.id, story_id=story.id)
            story.author.likes_count += 1
            db.session.add(like)

    def unlike_story(self, story):
        if self.has_liked_story(story):
            Storylikes.query.filter_by(
                user_id=self.id,
                story_id=story.id).delete()
            story.author.likes_count -= 1

    def has_liked_story(self, story):
        return Storylikes.query.filter(
            Storylikes.user_id == self.id,
            Storylikes.story_id == story.id).count() > 0
    # method to like and unlike stories and check if user has liked a story end

    # method to check if user has bookmarked a story
    def has_bookmarked_story(self, story):
        return Collection.query.filter(
            Collection.user_id == self.id,
            Collection.collection_id == story.id).count() > 0
    # method to check if user has bookmarked a story end

    # method to follow and unfollow users and check if user has followed another user
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0
    # method to follow and unfollow users and check if user has followed another user end

    # getting list of posts for a personalized timeline
    def followed_posts(self):
        followed = Story.query.join(
            followers, (followers.c.followed_id == Story.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Story.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Story.date_posted.desc())
    # getting list of posts for a personalized timeline end


# defining the representation state of the User class (Model)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.profile_pic}', '{self.profile_bg}')"
# defining the User class (Model) end


# defining the Post class (Model)
class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    story_image = db.Column(
        db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime, index=True, nullable=False,
                            default=datetime.utcnow)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    collections = db.relationship(
        'Collection', backref='story', cascade="all,delete", lazy=True)
    likes = db.relationship(
        'Storylikes', backref='story', cascade="all,delete", lazy='dynamic')

# defining the representation state of the Post class (Model)
    def __repr__(self):
        return f"Story('{self.title}', '{self.date_posted}', '{self.author}', '{self.likes}')"
# defining the Post class (Model) end


# defining the storylikes (Model)
class Storylikes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    story_id = db.Column(
        db.Integer, db.ForeignKey('story.id'), nullable=False)
# defining the storylikes (Model) end


# defining the Collections class (Model)
class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    collection_id = db.Column(
        db.Integer, db.ForeignKey('story.id'), nullable=False)
    date_added = db.Column(db.DateTime, index=True, nullable=False,
                           default=datetime.utcnow)

# defining the representation state of the Collections class (Model)
    def __repr__(self):
        return f"Collection('{self.collection_id}', '{self.user_id}')"
# defining the Collections class (Model) end
