
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired



class Postform(FlaskForm):    
    title :str= StringField('Title', validators=[
                           DataRequired()])   

    content=TextAreaField('content',validators=[DataRequired()])
    sumbit = SubmitField(' post')