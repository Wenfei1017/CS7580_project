from eventmanager.events.model import Event
from flask import abort, Response, flash, redirect, render_template, url_for
from wtforms.fields.html5 import DateField, DateTimeField
from flask_login import login_user, current_user, logout_user
from eventmanager.events.model import EventEnum, StatusEnum
from eventmanager.users.model import User

from eventmanager.events.forms import EventForm, EventDetailForm, UpdateEventForm, SearchEventForm


from eventmanager.registrations.model import Registration
from eventmanager import db, bcrypt
from datetime import datetime
import requests
import json
import os
from eventmanager.events.utils import define_event_status 


def obj_to_rep(obj):
    return {
    'id': obj.id,
    'title': obj.title,
    'description': obj.description,
    'time_posted': str(obj.time_posted),
    'time_start': str(obj.time_start),
    'time_end': str(obj.time_end),
    'category': obj.category.name,
    'event_address': obj.event_address,
    'sponsor_id': obj.sponsor_id,
    'status' : obj.status
    }


def get_all_events():
    if current_user.is_anonymous or current_user.role.name == 'User':
        return Response('Method not allowed', 403)
    result = Event.query.all()
    for event in result:
        if datetime.now() < event.time_start:
            event.status = 'Starting_soon'
        elif datetime.now() > event.time_end:
            event.status = 'Finished'
        else:
            event.status = 'Opening_now'
    return json.dumps([obj_to_rep(r) for r in result])


def get_events_by_user_id(user_id):
    if current_user.is_anonymous or current_user.role.name == 'Sponsor' or current_user.id != user_id:
        return Response('Method not allowed', 403)
    registrations = Registration.query.filter_by(user_id=current_user.id).all()
    events=[]
    for registration in registrations:
        event = Event.query.get_or_404(registration.event_id)
        events.append(event)

    res = json.dumps([obj_to_rep(e) for e in events])
    return json.dumps(res)


def create_event(payload):
    if current_user.is_anonymous or current_user.role.name == 'User':
        return Response('Method not allowed', 403)
    if payload['category'] not in EventEnum.__members__:
        return Response('this category does not exist', 400)
    event = Event(title=payload['title'], description=payload['description'], event_address=payload['event_address'], category=payload['category'])
    event.time_start = datetime.strptime(payload.get('time_start'), "%m/%d/%Y %H:%M:%S")
    event.time_end = datetime.strptime(payload.get('time_end'), "%m/%d/%Y %H:%M:%S")
    event.sponsor_id = current_user.id
    db.session.add(event)
    db.session.commit()
    return Response('event create successful', 200)


def event_update(event_id, payload):
    if current_user.is_anonymous or current_user.role.name == 'User':
        return Response('Method not allowed', 403)
    event = Event.query.get_or_404(event_id)
    if event.sponsor_id != current_user.id:
        return ('Unauthorized', 405)
    event.title = payload['title']
    event.description = payload['description']
    event.event_address = payload['event_address']
    event.category = payload['category']
    event.time_start = datetime.strptime(payload['time_start'], "%m/%d/%Y %H:%M:%S")
    event.time_end = datetime.strptime(payload['time_end'], "%m/%d/%Y %H:%M:%S")
    db.session.add(event)
    db.session.commit()
    return Response('update successfully', 200)


def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    define_event_status(event)
    return json.dumps(obj_to_rep(event))

def get_all_in_category(category):
    if category not in EventEnum.__members__:
        return Response('this category does not exist', 400)
    result = Event.query.filter_by(category=category)
    for event in result:
        define_event_status(event)
    return json.dumps([obj_to_rep(obj) for obj in result])


def get_event_by_status(status):
    if status not in StatusEnum.__members__:
        return Response('this status does not exist', 400)
    if status == 'Starting_soon':
        result = Event.query.filter(Event.time_start > datetime.now())
    elif status == 'Finished':
        result = Event.query.filter(Event.time_end < datetime.now())
    else:
        result = Event.query.filter(Event.time_start < datetime.now(), Event.time_end > datetime.now())
    
    return json.dumps([obj_to_rep(obj) for obj in result])


def event_delete(event_id):
    if current_user.is_anonymous or current_user.role.name == 'User':
        return Response('Method not allowed', 403)
    event = Event.query.get_or_404(event_id)
    if event.sponsor_id != current_user.id:
        abort(403)
    db.session.delete(event)
    db.session.commit()
    return Response('delete successfully', 200)


def sort_events(request):
    criteria = request.args.get('sort_by')
    events = Event.query.all()
    if criteria == 'time_start':
        current_time = datetime.utcnow()
        events_sorted = sorted(events, key=lambda x: abs(x.time_start - current_time))
        return json.dumps([obj_to_rep(obj) for obj in events_sorted])
    elif criteria == 'location':
        cur_loc = get_current_location()
        events_sorted = sort_by_dis(events, cur_loc)
        return json.dumps([obj_to_rep(obj) for obj in events_sorted])
    else:
        return Response('Order criteria is not supported', 400)


def search_events(request):
    time_start = request.args.get('time_start')
    time_end = request.args.get('time_end')
    location = request.args.get('location')
    result = Event.query.all()
    if time_start is not None:
        time_start_dt = datetime.strptime(time_start, "%m/%d/%Y %H:%M:%S")
        result = filter(lambda x: x.time_start > time_start_dt, result)
    if time_end is not None:
        time_end_dt = datetime.strptime(time_end, "%m/%d/%Y %H:%M:%S")
        result = filter(lambda x: x.time_end < time_end_dt, result)
    if location is not None:
        result = filter(lambda x: x.event_address.find(location) != -1, result)
    return json.dumps([obj_to_rep(obj) for obj in result])


def search_events_ui(request):
    form = SearchEventForm()
    result = Event.query.all()
    if form.validate_on_submit():
        time_start = form.search_by_time_start.data
        time_end = form.search_by_time_end.data
        title = form.search_by_title.data
        location = form.search_by_loc.data

        if time_start is not None:
            result = list(filter(lambda x: x.time_start > time_start, result))
        if time_end is not None:
            result = list(filter(lambda x: x.time_end < time_end, result))
        if location is not None:
            result = list(filter(lambda x: x.event_address.find(location) != -1, result))
        if title is not None:
            result = list(filter(lambda x: x.title.find(title) != -1, result))
        return render_template('home_after_search.html', events=result)
    return render_template('search_events.html', title='Search Events', form=form)


def get_current_location():
    geo = requests.post('https://www.googleapis.com/geolocation/v1/geolocate', params={'key': os.environ.get('GOOGLEMAPS_KEY')})
    lat = str(geo.json()['location']['lat'])
    lng = str(geo.json()['location']['lng'])
    loc = requests.get('https://maps.googleapis.com/maps/api/geocode/json',
                       params={
                           'key': os.environ.get('GOOGLEMAPS_KEY'),
                           'latlng': lat+','+lng
                       })
    loc_text = loc.json()['results'][0]['formatted_address']
    return loc_text


def cal_dis(loc1, loc2):
    dis = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json',
                       params={
                           'key': os.environ.get('GOOGLEMAPS_KEY'),
                           'units': 'imperial',
                           'origins': loc1,
                           'destinations': loc2
                       })
    return dis.json()['rows'][0]['elements'][0]['distance']['value']


def sort_by_dis(events, cur_loc):
    events_sorted = sorted(events, key=lambda x: cal_dis(x.event_address, cur_loc))
    return events_sorted


def new_event_ui():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(title=form.title.data, description=form.description.data, event_address=form.event_address.data,
                      category=form.category.data)
        event.time_start = form.time_start.data
        event.time_end = form.time_end.data
        event.sponsor_id = current_user.id
        db.session.add(event)
        db.session.commit()
        flash('Your event has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_event.html', title='New Event',
                           form=form, legend='New Event')


def event_detail_ui(event_id):

    regis=[]
    if not current_user.is_anonymous:
        regis = Registration.query.filter_by(user_id=current_user.id)

    registrations=Registration.query.filter_by(event_id=event_id)
    event = Event.query.get_or_404(event_id)

    return render_template('event.html', title='Event', registrations=registrations, regis=regis, event=event, current=datetime.utcnow())


def my_events_ui(request):
    print(1)

    page = request.args.get('page', 1, type=int)
    if current_user.is_anonymous:
        return Response('Please log in first', 403)
    if current_user.role.name == 'Sponsor':
        return Response('Please log in as User first', 403)
    event_id = request.args.get('event_id')
    event = Event.query.get_or_404(event_id)
    if Registration.query.get((current_user.id, event_id)):
        flash('Your have already been registered!', 'success')
        #        return 'already registered', 400
    else:
        registration = Registration(user_id=current_user.id, event_id=event_id)
        db.session.add(registration)
        db.session.commit()
    registrations = Registration.query.filter_by(user_id=current_user.id).paginate(page=page, per_page=5)
    return render_template('my_events.html', registrations=registrations)


def my_event_update_ui(request):
    form = UpdateEventForm()
    event_id = request.args.get('event_id')
    event = Event.query.get_or_404(event_id)
    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.event_address = form.event_address.data
        event.category = form.category.data
        event.time_start = form.time_start.data
        event.time_end = form.time_end.data
        event.sponsor_id = current_user.id
        db.session.add(event)
        db.session.commit()
        flash('Your event has been updated!', 'success')
        return redirect(url_for('events.my_events_ui'))
    elif request.method == 'GET':
        form.title.data = event.title
        form.description.data = event.description
        form.time_start.data = event.time_start
        form.time_end.data = event.time_end
        form.event_address.data = event.event_address
    return render_template('create_event.html', title='Update Event',
                           form=form, legend='Update Event')


def delete_my_event_ui(event_id):
    if current_user.is_anonymous or current_user.role.name == 'User':
        return Response('Method not allowed', 403)
    event = Event.query.get_or_404(event_id)
    if event.sponsor_id != current_user.id:
        abort(403)
    db.session.delete(event)
    db.session.commit()
    registrations = Registration(user_id=current_user.id, event_id=event_id)
    flash('The event has been deleted succussfullt', 'success')
    return render_template('my_events.html', events=registrations)


def latest_event_ui(request):
    page = request.args.get('page', 1, type=int)
    registrations = Event.query.order_by(Event.time_posted.desc()).limit(5).paginate(page=page, per_page=5)
    return render_template('my_events.html', events=registrations)


def show_announcement_ui():
    return render_template('announcement.html')


def my_events_regis_ui(request):
    page = request.args.get('page', 1, type=int)
    if current_user.is_anonymous:
        return Response('Please log in first', 403)
    if current_user.role.name == 'Sponsor':
        registrations = Event.query.filter_by(sponsor_id=current_user.id).paginate(page=page, per_page=5)
        return render_template('my_create_events.html', events=registrations)
    else:
        registrations = Registration.query.filter_by(user_id=current_user.id).paginate(page=page, per_page=5)

        return render_template('my_events.html', events=registrations)


def near_me_event_ui(request):
    events = Event.query.all()
    cur_loc = get_current_location()
    print(cur_loc)
    events_sorted = sorted(events, key=lambda x: cal_dis(x.event_address, cur_loc))
    print(events_sorted)
    return render_template('near_me.html', nearevents=events_sorted)

