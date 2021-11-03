from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email

class UrlForm(FlaskForm):
    url = StringField("URL: ", validators=[DataRequired()])
    submit = SubmitField("Submit")