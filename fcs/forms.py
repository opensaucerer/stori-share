# importing the required modules
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_ckeditor import CKEditorField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from fcs.models import User
from flask_login import current_user
# importing the required modules end

# forbiden usernames to allow for routes consistency
FORBIDEN_NAMES = ['signin', 'signup', 'signout', 'about', 'collections']


# defining the registration form class
class RegistrationForm(FlaskForm):

    username = StringField("Username", validators=[
        DataRequired(), Length(min=3, max=10, message="Username must be between 3 and 10 characters")], render_kw={
        'autocomplete': 'username'})
    email = StringField("Email", validators=[DataRequired(), Email()], render_kw={
        'autocomplete': 'email'})
    password = PasswordField("Password", validators=[Length(min=4, message="Password must be at least 4 characters"), DataRequired()], render_kw={
                             'autocomplete': 'new-password'})
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(), EqualTo("password", message="Your Passwords Don't Match")], render_kw={
        'autocomplete': 'new-password'})
    submit = SubmitField('Sign Up')

    # setting up custom validation to check if username exists
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data.lower()).first()
        if user or username.data.lower() in FORBIDEN_NAMES:
            raise ValidationError('That Username Has Been Taken')

    # setting up custom validation to check if email exists
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.lower()).first()
        if user:
            raise ValidationError('That Email Has Been Taken')
# defining the registration form class end


# defining the login form class end
class LoginForm(FlaskForm):

    email = StringField("Email", validators=[DataRequired(), Email()], render_kw={
        'autocomplete': 'email'})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={
                             'autocomplete': 'current-password'})
    remember_me = BooleanField("Remember Me")
    submit = SubmitField('Sign In')
# defining the login form class end


# defining class for story form
class StoryForm(FlaskForm):

    title = StringField("Give Your Story A Title", validators=[
                        DataRequired(), Length(max=80, message="Your Title is Too Long")], render_kw={
        'placeholder': 'Something Short and Catchy'})

    content = TextAreaField("Tell Your Story In Detail",
                            validators=[DataRequired(), Length(min=100, message="Your Story is Too Short")], render_kw={
                                'placeholder': 'Remember, Any Story Can Be Told'})

    # post_image = SelectField("Add A Story Image", validators=[DataRequired()])
    submit = SubmitField('Publish')
# defining class for story form end


# defining the update profile form class
class ProfileForm(FlaskForm):

    username = StringField("Username", validators=[
        DataRequired(), Length(min=3, max=10, message="Username must be between 3 and 10 characters")], render_kw={
        'autocomplete': 'username'})
    email = StringField("Email", validators=[DataRequired(), Email()], render_kw={
        'autocomplete': 'username'})
    about = TextAreaField("About")
    profile_pic = FileField('Profile Picture', validators=[
                            FileAllowed(['png', 'jpg', 'jpeg'], message="You can only upload image files with png, jpg, jpeg")], render_kw={
                                'for': 'profile_pic'})
    profile_bg = FileField('Background Picture', validators=[
        FileAllowed(['png', 'jpg', 'jpeg'], message="You can only upload image files with png, jpg, jpeg")], render_kw={
        'for': 'profile_bg'})
    save = SubmitField('Save')

    # setting up custom validation to check if username exists
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data.lower()).first()
            if user:
                raise ValidationError('That Username Has Been Taken')

    # setting up custom validation to check if email exists
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data.lower()).first()
            if user:
                raise ValidationError('That Email Has Been Taken')
# defining the profile form class end
