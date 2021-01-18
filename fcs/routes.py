# importing requiered modules
import os
import secrets
from datetime import datetime
from flask import Flask, render_template, url_for, redirect, flash, jsonify, request
from werkzeug.utils import secure_filename
from fcs import app, db, bcrypt
from fcs.forms import RegistrationForm, LoginForm, StoryForm, ProfileForm
from fcs.models import User, Story, Collection, Storylikes
from fcs.exceptions import RequestError
from fcs.others import generate_url
from flask_login import login_user, current_user, logout_user, login_required
from flask_cors import CORS, cross_origin
# importing required modules end


# defining config variables
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
current_year = datetime.now().year
# defining config variables end


# stories feed / home route
@app.route('/')
def home():

    # defining variables
    form = LoginForm()
    story = Story
    posts = Story.query.order_by(Story.date_posted.desc()).all()
    # defining variables end

    return render_template('home.html', posts=posts, story=story, form=form, current_year=current_year)


# about route
@ app.route('/about')
def about():
    # defining variables
    blog_title = "About | Everyone Has A Story To Tell"
    # defining variables end

    return render_template('about.html', title=blog_title)


# registration route
@ app.route('/signup', methods=["POST", "GET"])
def register():
    # defining variables
    form = RegistrationForm()
    blog_title = "Sign Up | We Can't Wait to Read Your Stories"
    # defining variables end

    # redirecting using for accessing page if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('dashboard', username=current_user.username))
    # redirecting using for accessing page if already logged in end

        # Validating form on submit
    if form.validate_on_submit():
        # generating the user's profile background image
        bg_url = generate_url()
        # generating the user's profile background image end

        # generating hashed password
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        # generating hashed password end

        # add new user to User model
        new_user = User(username=form.username.data.lower(),
                        email=form.email.data.lower(), password=hashed_password, profile_bg=bg_url)
        # add new user to User model end

        # adding new user to database
        db.session.add(new_user)
        db.session.commit()
        # adding new user to database end

        # sending flased message
        flash(
            "Account Created Successfully", "success")
        # sending flased message end

        # redirecting user to login page
        return redirect(url_for('login'))
        # redirecting user to login page end

       # Validating form on submit end

    return render_template('register.html', form=form, title=blog_title, current_year=current_year)


# login route
@ app.route('/signin', methods=["POST", "GET"])
def login():

    user_data = request.get_json()

    # defining variables
    form = LoginForm()
    blog_title = "Sign In | Start Telling Your Stories"
    # defining variables end

    if user_data:
        email = user_data['email']
        password = user_data['password']
        remember_me = user_data['remember_me']
        existing_user = User.query.filter_by(email=email.lower()).first()

        if existing_user and bcrypt.check_password_hash(existing_user.password, password):
            # logging user in using flask login (login_user) for session management
            login_user(existing_user, remember=remember_me)
            return jsonify({"message": "Login Successful"}), 200
        elif existing_user:
            raise RequestError('Invalid Password')
        else:
            raise RequestError('Invalid Credentials')

    # redirecting using for accessing page if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('dashboard', username=current_user.username))
    # redirecting using for accessing page if already logged in end

    # Validating form on submit
    if form.validate_on_submit():
        # checking if user exists
        existing_user = User.query.filter_by(
            email=form.email.data.lower()).first()
        # checking if password matches signup password
        if existing_user and bcrypt.check_password_hash(existing_user.password, form.password.data):
            # logging user in using flask login (login_user) for session management
            login_user(existing_user, remember=form.remember_me.data)
            next_page = request.args.get("next")
            # sending flased message
            flash("Login Successful", "success")
            # logging user in using flask login (login_user) for session management end
            # redirecting user to dashboard
            return redirect(next_page) if next_page else redirect(url_for('dashboard', username=existing_user.username))
            # redirecting user to dashboard end

        # checking if user exists end
        elif existing_user:
            flash("Invalid Sign In Password", "danger")
        else:
            flash("That User Does not Exist", "danger")
        # checking if password matches signup password end
            # sending flased message end

    # Validating form on submit end
    return render_template('login.html', form=form, title=blog_title, current_year=current_year)


# logout route
@ app.route('/signout')
@ login_required
def logout():
    # logging out user
    logout_user()
    # redirecting to homepage
    return redirect(url_for('home'))
    # logging out user


def pic_save(image):
    random_name = secrets.token_hex(7)
    _, f_ext = os.path.splitext(image.filename)
    image_name = random_name + f_ext
    image_path = os.path.join(
        app.root_path, 'static/img/profile_pic', image_name)
    image.save(image_path)
    return image_name


def bg_save(image):
    random_name = secrets.token_hex(7)
    _, f_ext = os.path.splitext(image.filename)
    image_name = random_name + f_ext
    image_path = os.path.join(
        app.root_path, 'static/img/profile_bg', image_name)
    image.save(image_path)
    return image_name


# dashboard route
@ app.route('/<username>', methods=["GET", "POST"])
def dashboard(username):
    # getting url parameters (args)
    status = request.args.get("status")

    # getting user from database
    user = User.query.filter_by(username=username).first()
    # getting user from database

    # allowing access only if user exist
    if user:
        # defining variables
        if len(user.profile_bg.split("//")) > 1:
            bg_img = user.profile_bg

        else:
            bg_img = url_for(
                'static', filename='img/profile_bg/' + user.profile_bg)

        story = Story
        storylikes = Storylikes
        posts = Story.query.filter_by(user_id=user.id).order_by(
            Story.date_posted.desc())
        blog_title = f"@{username} Stories In One View"
        form = ProfileForm()
        login_form = LoginForm()
        about = user.about
        post_count = posts.count()
        profile_pic = url_for(
            'static', filename='img/profile_pic/' + user.profile_pic)
        # defining variables end

        # submitting profile form
        if form.validate_on_submit():
            # commiting changes to database
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.about = form.about.data
            if form.profile_pic.data:
                pic_path = pic_save(form.profile_pic.data)
                current_user.profile_pic = pic_path
            if form.profile_bg.data:
                bg_path = bg_save(form.profile_bg.data)
                current_user.profile_bg = bg_path
            db.session.commit()
            # commiting changes to database end

            # flashing message
            flash('Your Profile Was Updated', 'success')

            # redirecting user
            return redirect("/" + current_user.username + '#success')

        # populating form with user's default data
        elif request.method == "GET":
            if current_user.is_authenticated:
                form.username.data = current_user.username
                form.email.data = current_user.email
                form.about.data = current_user.about
            # populating form with user's default data end

        # checking if URL Parameter exisits before rendring
        if status == 'new-post':
            flash('Your Story is Live', 'success')
            return render_template('dashboard.html', title=blog_title, about=about, username=username, bg_img=bg_img, profile_pic=profile_pic, posts=posts, form=form, login_form=login_form, story=story, storylikes=storylikes, post_count=post_count, user=user)
        elif status == 'updated-post':
            flash('Your Story Has Been Updated', 'success')
            return render_template('dashboard.html', title=blog_title, about=about, username=username, bg_img=bg_img, profile_pic=profile_pic, posts=posts, form=form, login_form=login_form, story=story, storylikes=storylikes, post_count=post_count, user=user)
        else:
            return render_template('dashboard.html', title=blog_title, about=about, username=username, bg_img=bg_img, profile_pic=profile_pic, posts=posts, form=form, login_form=login_form, story=story, storylikes=storylikes, post_count=post_count, user=user)
        # checking if URL Parameter exisits before rendring end

    else:
        flash('That User Does Not Exist', 'danger')
        return redirect(url_for('home'))
    # allowing access only if user exist end


# New story route
@ app.route('/stories/new', methods=["POST", "GET"])
@ login_required
def new_story():
    # defining variables
    blog_title = "New Story | Let's Get Your Story Live"
    form = StoryForm()

    return render_template('new_story.html', title=blog_title, form=form)


# route for getting new stories
@ app.route('/stories/create_story', methods=["POST", "GET"])
@ login_required
def create_story():
    # getting story from json
    data = request.get_json()

    if data:

        # add new Story to User model
        new_story = Story(title=data['story_title'], content=data['story_content'],
                          story_image=data['story_image'], author=current_user)
        # add new Story to User model end

        # adding new Story to database
        db.session.add(new_story)
        db.session.commit()
        # adding new Story to database end

        # conmputing and returning message
        message = {"status": "success", "link": "/" +
                   current_user.username + "?status=new-post"}
        return jsonify(message), 201
        # computing and returning message end
    else:
        raise RequestError('failed')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_image(image):
    random_name = secrets.token_hex(7)
    _, f_ext = os.path.splitext(image.filename)
    image_name = random_name + f_ext
    image_path = os.path.join(
        app.root_path, 'static/img/story_image', image_name)
    image.save(image_path)
    return image_name


# route for getting new stories
@ app.route('/stories/story_upload', methods=["POST"])
@ login_required
def story_upload():

    if request.method == "POST":

        # getting story from json

        if request.files['story_image'] and allowed_file(request.files['story_image'].filename):

            story_image = save_image(request.files['story_image'])

            if story_image:
                # conmputing and returning message
                message = {"status": "success", "path": story_image}
                return jsonify(message), 200
                # computing and returning message end
            else:
                message = {"status": "failed"}
                return jsonify(message), 400
        else:
            message = {"status": "failed to unpack image"}
            return jsonify(message), 400


# Like Story route
@ app.route('/stories/like/<story_id>/<action>', methods=["POST", "GET"])
@ login_required
def add_like(story_id, action):
    # getting story from db
    story = Story.query.get(story_id)

    # checking if story exists
    if story:
        if action == 'like':
            # adding like to db
            current_user.like_story(story)
            new_likes = story.likes.count()
            db.session.commit()
            # adding new like end
            message = {"count": new_likes, "status": "success",
                       "total_count": story.author.likes_count}
            db.session.commit()
            return jsonify(message), 201

        if action == 'unlike':
            current_user.unlike_story(story)
            new_likes = story.likes.count()
            message = {"count": new_likes, "status": "success",
                       "total_count": story.author.likes_count}
            db.session.commit()
            return jsonify(message), 201

    else:
        message = {"status": "failed"}
        return jsonify(message), 400


# read story route
@ app.route('/stories/<id>/<title>')
def story(id, title):
    # defining variables
    # posts = Story.query.all()
    id = int(id)
    story = Story.query.get(id)
    form = LoginForm()
    # defining variables end

    # checking if the story exist
    if story:
        blog_title = Story.query.get(id).title
        return render_template('story.html', title=blog_title, story=story, form=form)

    else:
        flash("We Couldn't Find That Story", 'danger')
        return redirect(url_for('home'))


# edit story route
@ app.route('/edit_story/<id>/edit', methods=["POST", "GET"])
@ login_required
def edit_story(id):

    if request.method == 'POST':
        # getting story from json
        data = request.get_json()
        story_id = data['story_id']
        title = data['story_title']
        content = data['story_content']

        existing_story = Story.query.get(story_id)
        if existing_story:
            # Updating existing story
            existing_story.title = title
            existing_story.content = content
            if data['story_image']:
                existing_story.story_image = data['story_image']
            #  Updating existing story end
            # committing to database
            db.session.commit()
            # committing to database end
            # conmputing and returning message
            message = {"status": "success", "link": "/" +
                       current_user.username + "?status=updated-post"}
            return jsonify(message), 201
            # computing and returning message end

    if request.method == 'GET':
        # defining variables
        blog_title = "Edit Story | Your Story In a New Way"
        form = StoryForm()
        id = int(id)
        if Story.query.get(id):
            content = Story.query.get(id).content
            story_title = Story.query.get(id).title
            form.title.data = story_title
        else:
            return redirect(url_for('home'))

        return render_template('edit_story.html', title=blog_title, form=form, content=content, story_title=story_title)


# read story route
@ app.route('/delete_story/<id>', methods=["POST"])
@ login_required
def delete_story(id):
    # getting story from db
    story = Story.query.get(id)
    if story and current_user == story.author:
        # deleting story from db
        story.author.likes_count -= story.likes.count()
        db.session.delete(story)
        db.session.commit()
        flash("Your Story Was Deleted", "success")
        return redirect(url_for('dashboard', username=current_user.username))
    else:
        flash("We Couldn't Find That Story", "danger")
        return redirect(url_for('dashboard', username=current_user.username))


# add to collections route
@ app.route('/collections/<story_id>/<action>', methods=["POST", "GET"])
@ login_required
def mod_collections(story_id, action):
    # getting story from db
    story = Story.query.get(story_id)
    # checking if story exists
    if story:
        if action == 'add':
            # checking if collection exists
            exisiting_collection = Collection.query.filter_by(
                user_id=current_user.id, collection_id=story.id).first()
            if exisiting_collection:
                raise RequestError('failed')
            # adding story to collections
            new_collection = Collection(
                collection_id=story.id, user_id=current_user.id)
            db.session.add(new_collection)
            db.session.commit()
            # adding new collection end
            message = {"message": "success"}
            return jsonify(message), 201

        if action == 'remove':
            collection = Collection.query.filter_by(
                user_id=current_user.id, collection_id=story.id).first()
            db.session.delete(collection)
            db.session.commit()
            message = {"message": "success"}
            return jsonify(message), 201

    else:
        raise RequestError('failed')


# view collections route
@ app.route('/collections')
@ login_required
def collections():
    # defining variables
    blog_title = "Collections | All The Stories You Love"

    # getting collections from db
    story = Story
    collections = Collection.query.filter_by(
        user_id=current_user.id).order_by(Collection.date_added.desc())

    collection_count = collections.count()

    return render_template('collections.html', title=blog_title, collections=collections, story=story, collection_count=collection_count)


# follow users route
@ app.route('/follow', methods=['POST'])
@ login_required
def follow():

    # defining variables
    data = request.get_json()
    username = data['username']
    action = data['action']

    # getting user from the db
    user_to_follow = User.query.filter_by(username=username).first()

    # validating the user's existence
    if user_to_follow is None:
        raise RequestError('user not found')

    if user_to_follow == current_user:
        raise RequestError('you cannot follow yourself')

    # following the user
    if action == 'follow':
        current_user.follow(user_to_follow)
        db.session.commit()
        return jsonify({"message": "success", "username": username, "count": user_to_follow.followers.count()}), 201

    # unfollowing the user
    if action == 'unfollow':
        current_user.unfollow(user_to_follow)
        db.session.commit()
        return jsonify({"message": "success", "username": username, "count": user_to_follow.followers.count()}), 201


# followers users route
@ app.route('/<username>/followers', methods=['GET'])
@ login_required
def followers(username):

    # defining variables
    blog_title = f"See Those Who Love @{username} stories"

    # querying followers from db
    user = User.query.filter_by(username=username).first()
    followers = user.get_followers()

    return render_template('followers_following.html', title=blog_title, user=user, followers=followers)


# following users route
@ app.route('/<username>/following', methods=['GET'])
@ login_required
def following(username):

    # defining variables
    blog_title = f"See Creators @{username} Love"

    # querying data from db
    user = User.query.filter_by(username=username).first()
    followers = user.get_following()

    return render_template('followers_following.html', title=blog_title, user=user, followers=followers)
