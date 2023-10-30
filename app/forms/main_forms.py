from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, TelField, TextAreaField, BooleanField, SubmitField, DateField, DateTimeField, URLField, DateTimeLocalField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, InputRequired, Length, ValidationError, EqualTo, Email

class PostForm(FlaskForm):
    """Post Form: body:Text, Submit:Btn"""
    body = TextAreaField('Post',
                            validators=[
                                DataRequired(), Length(min=1, max=280)],
                            render_kw={'class': 'textArea',
                                    'placeholder': ' What is happening?!'}
                            )
    post_picture = FileField('Post Picture', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp', 'gif'])], render_kw={'class': ''})
    submit = SubmitField('Post', render_kw={'class': 'btn-form'})

class RegisterForm(FlaskForm):
    """Registeration Form: username, email, Phone_Number, Password, Submit btn"""
    username = StringField('Name', validators=[
        DataRequired(), Length(min=2, max=20)], render_kw={'class': 'formField', 'placeholder': ' Display Name'})
    email = EmailField('Email', validators=[DataRequired()], render_kw={'class': 'formField',
                        'placeholder': ' Email'})
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=6, max=20)], render_kw={'class': 'formField', 'placeholder': ' Password'})
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), Length(min=6, max=20)], render_kw={'class': 'formField', 'placeholder': ' Confirm Password'})
    profile_picture = FileField('Profile Picture', validators=[
                                FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')], render_kw={'class': ''})

    submit = SubmitField('Register', render_kw={'class': 'btn-form'})

class EditRegister(FlaskForm):
    """Edit Form: username, email, Phone_Number, Password, Submit btn"""
    username = StringField('Name', validators=[
        DataRequired(), Length(max=20)], render_kw={'class': 'formField', 'placeholder': ' Display Name'})
    email = EmailField('Email', validators=[DataRequired()], render_kw={'class': 'formField',
                        'placeholder': ' Email'})
    phone_number = TelField('Phone Number', validators=[Length(min=6, max=20)], render_kw={'class': 'formField',
                            'placeholder': ' Phone Number'})
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=6, max=20)], render_kw={'class': 'formField', 'placeholder': ' Password'})
    profile_picture = FileField('Profile Picture', validators=[
                                FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')], render_kw={'class': ''})
    header_picture = FileField('Profile Picture', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')], render_kw={'class': ''})

    bio = TextAreaField('Bio', validators=[Length(min=1, max=280)], render_kw={
                        'class': 'textArea', 'placeholder': ' Bio'})
    location = StringField('Location', validators=[Length(min=2, max=20)], render_kw={
                            'class': 'formField', 'placeholder': ' Location'})
    birthday = DateField('Birthday', render_kw={
                            'class': '', 'placeholder': ' Birthday'})
    url = URLField('Website', render_kw={
                    'class': 'formField', 'placeholder': ' Website'})

    submit = SubmitField('Save', render_kw={'class': 'btn-form'})

    def validate_user_email(self, email):
        """Validating if user already Existed"""
        existing_user_email = User.query.filter_by(
            email=email.data).first()
        if existing_user_email:
            raise ValidationError(
                "That email already exist. Please choose a diffent one.")

class EditProfile(FlaskForm):
    username = StringField('Name', validators=[DataRequired(), Length(
        min=2, max=20)], render_kw={'class': 'formField', 'placeholder': ' Display Name'})
    bio = TextAreaField('Bio', validators=[Length(max=80)], render_kw={
                        'class': 'textArea', 'placeholder': ' Bio'})
    location = StringField('Location', validators=[Length(max=20)], render_kw={
                            'class': 'formField', 'placeholder': ' Location'})
    birthday = DateField('Birthday', render_kw={
                            'class': '', 'placeholder': ' Birthday'})

    submit = SubmitField('Save', render_kw={'class': 'btn-form'})

    def validate_bio(self, field):
        # Check if the field is empty or contains only whitespace
        if field.data is not None and not field.data.strip():
            field.data = None

class EditURL(FlaskForm):
    url = URLField('Website', render_kw={
        'class': 'formField', 'placeholder': ' Website'})
    submit = SubmitField('Save', render_kw={'class': 'btn-form'})

class EditBirthday(FlaskForm):
    birthday = DateField('Birthday', render_kw={
                            'class': '', 'placeholder': ' Birthday'})
    submit = SubmitField('Save', render_kw={'class': 'btn-form'})

class EditProfilePic(FlaskForm):
    profile_picture = FileField('Profile Picture', validators=[
                                FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')], render_kw={'class': ''})

    submit = SubmitField('Save', render_kw={'class': 'btn-form'})

class EditHeaderPic(FlaskForm):
    header_picture = FileField('Profile Picture', validators=[
                                FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')], render_kw={'class': ''})

    submit = SubmitField('Save', render_kw={'class': 'btn-form'})

class LoginForm(FlaskForm):
    """Login Form: email, Password, login-btn"""
    email = EmailField('Email', validators=[DataRequired()], render_kw={
        'class': 'formField',
                        'placeholder': ' Email'})
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=6, max=20)], render_kw={'class': 'formField', 'placeholder': ' Password'})
    submit = SubmitField('Login', render_kw={'class': 'btn-form'})

class CommentForm(FlaskForm):
    """Comment Form: TextArea - Submit-btn"""
    comment = TextAreaField('Post',
                            validators=[
                                DataRequired(), Length(min=1, max=280)],
                            render_kw={'class': 'textArea',
                                        'placeholder': ' Post your reply!'}
                            )
    submit = SubmitField('Submit', render_kw={'class': 'btn-form'})