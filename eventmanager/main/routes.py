from flask import render_template, request, Blueprint
from eventmanager.events.model import Event
from eventmanager.registrations.model import Registration

from eventmanager import cache
import os


main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)

    registrations = Registration.query.order_by(Registration.registration_time.desc()).paginate(page=page, per_page=5)
    # Only use cache when cache server exist
    cache_servers = os.environ.get('MEMCACHIER_SERVERS')
    if cache_servers is None:
        events = Event.query.order_by(Event.time_posted.desc()).paginate(page=page, per_page=5)
    else:
        events = get_all_events(page)

    return render_template('home.html', events=events, registrations=registrations)


@main.route("/about")
def about():
    return render_template('about.html', title='about')


@cache.memoize()
def get_all_events(page):
    events = Event.query.order_by(Event.time_posted.desc()).paginate(page=page, per_page=5)
    return events
