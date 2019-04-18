from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField

from wtforms.validators import DataRequired, InputRequired, Optional
from wtforms.fields import DateField, DateTimeField

from datetime import datetime


class EventForm(FlaskForm):
    # id = IntegerField('Id', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    time_posted = DateField('Posted time', format='%m/%d/%Y', default=datetime.utcnow)
    time_start = DateTimeField('Start time', format='%m/%d/%Y %H:%M:%S', validators=[InputRequired()], default=datetime.utcnow)
    time_end = DateTimeField('End time', format='%m/%d/%Y %H:%M:%S', validators=[InputRequired()], default=datetime.utcnow)
    event_address = StringField('Address', validators=[DataRequired()])
    category = SelectField('Event Category', choices=[
        ('beer_and_wine', 'Bear and Wine'), ('beauty', 'Beauty'), ('coffee', 'Coffee'), ('reading', 'Reading'),
        ('outside', 'Outside'), ('pets', 'Pets'), ('sports', 'Sports'), ('others', 'Others')])
    submit = SubmitField('Post')



class SearchEventForm(FlaskForm):
    search_by_title = StringField('Search Title', validators=[Optional()])
    search_by_time_start = DateTimeField('Start From Time', format='%m/%d/%Y %H:%M:%S', validators=[Optional()], default=datetime.utcnow)
    search_by_time_end = DateTimeField('End From Time', format='%m/%d/%Y %H:%M:%S', validators=[Optional()])
    search_by_loc = StringField('Search Location', validators=[Optional()])
    submit = SubmitField('Search')




class EventDetailForm(FlaskForm):
    id = IntegerField('Id')
    title = StringField('Title')
    description = TextAreaField('Description')
    time_posted = DateField('Posted time', format='%m/%d/%Y', default=datetime.utcnow)
    time_start = DateTimeField('Start time', format='%m/%d/%Y %H:%M:%S', default=datetime.utcnow)
    time_end = DateTimeField('End time', format='%m/%d/%Y %H:%M:%S', default=datetime.utcnow)
    event_address = StringField('Address')
    category = SelectField('Event Category', choices=[
        ('beer_and_wine', 'Bear and Wine'), ('beauty', 'Beauty'), ('coffee', 'Coffee'), ('reading', 'Reading'),
        ('outside', 'Outside'), ('pets', 'Pets'), ('sports', 'Sports'), ('others', 'Others')])
    submit = SubmitField('Get')



class EventRegisterForm(FlaskForm):
    user_id = IntegerField('Id')
    event_id = IntegerField('Id')
    submit = SubmitField('Post')



class UpdateEventForm(FlaskForm):
    id = IntegerField('Id')
    title = StringField('Title')
    description = TextAreaField('Description')
    time_posted = DateField('Posted time', format='%m/%d/%Y', default=datetime.utcnow)
    time_start = DateTimeField('Start time', format='%m/%d/%Y %H:%M:%S', default=datetime.utcnow)
    time_end = DateTimeField('End time', format='%m/%d/%Y %H:%M:%S', default=datetime.utcnow)
    event_address = StringField('Address')
    category = SelectField('Event Category', choices=[
        ('beer_and_wine', 'Bear and Wine'), ('beauty', 'Beauty'), ('coffee', 'Coffee'), ('reading', 'Reading'),
        ('outside', 'Outside'), ('pets', 'Pets'), ('sports', 'Sports'), ('others', 'Others')])
    submit = SubmitField('Update')

