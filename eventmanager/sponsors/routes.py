from flask import render_template, url_for, flash, redirect, request, Blueprint
from eventmanager.events.model import Event
from eventmanager.sponsors.controller import *

sponsors = Blueprint('sponsors', __name__)

@sponsors.route("/sponsors", methods=['GET'])
def getSponsors():
    return get_all_sponsors()


@sponsors.route("/sponsor/<string:username>")
# todo
def sponsor_events(username):
    page = request.args.get('page', 1, type=int)
    sponsor = Sponsor.query.filter_by(username=username).first_or_404()
    events = Event.query.filter_by(author=sponsor)\
        .order_by(Event.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_events.html', events=events, sponsor=sponsor)
