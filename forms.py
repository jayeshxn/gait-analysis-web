# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, SelectField, DateField, FloatField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Optional

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], validators=[DataRequired()])
    height = FloatField('Height (cm)', validators=[DataRequired()])
    weight = FloatField('Weight (kg)', validators=[DataRequired()])
    gait_disorder = SelectField('Gait Disorder', choices=[('Left', 'Left'), ('Right', 'Right'), ('Both', 'Both'), ('Unknown', 'Unknown')], validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class UploadForm(FlaskForm):
    tag = StringField('Tag', validators=[DataRequired()])
    data = FileField('Dataset', validators=[DataRequired()])
    data_type = SelectField('Type of Data', choices=[('IMU', 'IMU'), ('EEG', 'EEG'), ('Others', 'Others')], validators=[DataRequired()])
    metadata = TextAreaField('Metadata (optional)', validators=[Optional()])
    submit = SubmitField('Upload')
