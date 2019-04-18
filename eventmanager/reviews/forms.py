from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, InputRequired
from wtforms.fields import DateField, DateTimeField
#from datetime import datetime
from datetime import datetime

class ReviewForm(FlaskForm):
    rating = SelectField('Rating', choices=[
        ("1","1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")])
    content = TextAreaField('Content', validators=[DataRequired()])
    review_time = DateTimeField('Review Time', format='%m/%d/%Y %H:%M:%S', default=datetime.utcnow)

    submit = SubmitField('Post')
