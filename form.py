from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

# Start of register Form


class RegistriationForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    Email = StringField('Email', validators=[
        DataRequired(), Length(min=2, max=20), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6, max=30)])
    confirmPassword = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password')])
    sumbit = SubmitField('Sign Up')
# end of register Form

# Start of login Form


class LoginForm(FlaskForm):

    Email = StringField('Email', validators=[
        DataRequired(), Length(min=2, max=20), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6, max=30)])
    remember = BooleanField('Remember me')
    sumbit = SubmitField('Login')
# end of login Form
