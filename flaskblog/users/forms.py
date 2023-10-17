from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import Users




class RegistriationForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    Email = StringField('Email', validators=[
        DataRequired(), Length(min=2, max=50), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6, max=30)])
    confirmPassword = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password')])
    sumbit = SubmitField('Sign Up')
    def validate_username(self, username) -> Users :
        user=Users.query.filter_by(Username=username.data).first()
        if user:
            raise ValidationError("that username is taken ,change it")
        
    def validate_Email(self, Email)->Users:
        email=Users.query.filter_by(Email=Email.data).first()
        if email:
            raise ValidationError("that email used before ")
# end of register Form

# Start of login Form


class LoginForm(FlaskForm):

    Email = StringField('Email', validators=[
        DataRequired(), Length(min=2, max=100), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6, max=30)])
    remember = BooleanField('Remember me')
    sumbit = SubmitField('Login')
# end of login Form

#account update form
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    Email = StringField('Email', validators=[
        DataRequired(), Length(min=2, max=100), Email()])
    picture =FileField('upload picture',validators=[FileAllowed(['jpg','png'])])
    sumbit = SubmitField('update')
    def validate_username(self, username):
        if username.data != current_user.Username:
            user = Users.query.filter_by(Username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')
        
    def validate_Email(self,    Email):
        if Email.data != current_user.Email:
            user = Users.query.filter_by(Email=Email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):

       Email = StringField('Email', validators=[
        DataRequired(), Length(min=2, max=100), Email()])
       sumbit = SubmitField('Request passowrd reset')
def validate_Email(self, Email)->Users:
        email=Users.query.filter_by(Email=Email.data).first()
        if email is None:
            raise ValidationError("there is no account with that email ")
        

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6, max=30)])
    confirmPassword = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password')])
    sumbit = SubmitField('Reset passowrd ')