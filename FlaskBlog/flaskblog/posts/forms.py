# All imports required

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

# Class to create forms inherited from the FlaskForm Class of the flask_wtf lib

class PostForm(FlaskForm):
    # declaring title as String field and making it required field
    title = StringField('Title', validators=[DataRequired()])
    # declaring content as Text Field and making it required field
    content = TextAreaField('Content', validators=[DataRequired()])
    # declaring submit as Submit field, essentially a button
    submit = SubmitField('Post')
