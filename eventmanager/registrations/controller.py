from flask import Response, abort, flash, request
from eventmanager.registrations.model import Registration
from flask import Response, url_for, render_template, redirect, flash
from eventmanager.events.model import Event
from eventmanager.registrations.model import Registration
from eventmanager import db
from flask_login import current_user
import json


def obj_to_rep(obj):
    return {
        'user_id': obj.user_id,
        'event_id': obj.event_id,
        'registration_time': str(obj.registration_time)
    }


def get_registration(request):
    if current_user.is_anonymous:
        return Response('Please log in first', 403)
    if current_user.role.name == 'Sponsor':
        return get_sponsor_registration(request)
    if current_user.role.name == 'User':
        return get_user_registration(request)


def delete_registration():
    if current_user.is_anonymous:
        return Response('Please log in first', 403)
    if current_user.role.name is not 'User':
        return Response('Please log in as User', 403)
    return delete_user_registration()
    # if current_user.role.name == 'Sponsor':
    #     return delete_sponsor_registration(event_id)
    # if current_user.role.name == 'User':
    #     return delete_user_registration()


def delete_registration_ui(event_id):
    if current_user.is_anonymous:
        return Response('Please log in first', 403)
    if current_user.role.name == 'User':
        return delete_user_registration_ui(event_id)


def get_sponsor_registration(request):
    event_id = request.args.get('event', type=int)
    user_id = request.args.get('user', type=int)
    if event_id is not None and user_id is not None:
        # todo comment for testing
        # event = Event.query.get_or_404(event_id)
        # if event.sponsor_id is not current_user.id:
        #     abort(403)
        registration = Registration.query.get_or_404((user_id, event_id))
        return Response(json.dumps(obj_to_rep(registration)), 200)
    elif event_id is not None:
        # todo comment for testing
        # event = Event.query.get_or_404(event_id)
        # if event.sponsor_id is not current_user.id:
        #     abort(403)
        registrations = Registration.query.filter_by(event_id=event_id).all()
        res = json.dumps([obj_to_rep(r) for r in registrations])
        return Response(res, 200)
    else:
        abort(403)


def get_user_registration(request):
    event_id = request.args.get('event', type=int)
    user_id = request.args.get('user', type=int)
    if event_id is None and user_id is None:
        registrations = Registration.query.filter_by(user_id=current_user.id).all()
        res = json.dumps([obj_to_rep(r) for r in registrations])
        return Response(res, 200)
    elif event_id is not None:
        registration = Registration.query.get_or_404((current_user.id, event_id))
        return Response(json.dumps(obj_to_rep(registration)), 200)
    else:
        abort(403)

def post_user_registration(payload):
    print("from here")
    print(payload)
    if current_user.is_anonymous:
        return Response('Please log in first', 403)
    if current_user.role.name == 'Sponsor':
        return Response('Please log in as User first', 403)
    event_id = payload['event_id']
    event = Event.query.get_or_404(event_id)
    if Registration.query.get((current_user.id, event_id)):
        return 'already registered', 400
    registration = Registration(user_id=current_user.id, event_id=event_id)
    db.session.add(registration)
    db.session.commit()
    return 'registered success', 201


#def post_user_registration(request):
#    if current_user.is_anonymous:
#        return Response('Please log in first', 403)
#    if current_user.role.name == 'Sponsor':
#        return Response('Please log in as User first', 403)
#    print(request)
#    event_id = request.args.get('event_id', type=int)
#    print(event_id)
#    print(request)
#    event = Event.query.get_or_404(event_id)
#    if Registration.query.get((current_user.id, event_id)):
#        return 'already registered', 400
#    registration = Registration(user_id=current_user.id, event_id=event_id)
#    db.session.add(registration)
#    db.session.commit()
#    flash('You are in!', 'success')
#    return 'registered success', 201



# # todo Not sure if a sponsor has the privilege to remove a user's registration
# payload -> event_id
# def delete_sponsor_registration(payload):
#     event_id = payload['event_id']
#     user_id = payload['user_id']
#     # todo comment for testing
#     # event = Event.query.get_or_404(event_id)
#     # if event.sponsor_id is not current_user.id:
#     #     abort(403)
#     registration = Registration.query.get_or_404((user_id, event_id))
#     db.session.delete(registration)
#     db.session.commit()
#     return 'unregistered success', 200

def delete_user_registration():
    event_id=request.args.get("event", type=int)
    # registration = Registration.query.get_or_404({"user_id": current_user.id, "event_id": event_id})
    registration = Registration.query.get_or_404((current_user.id, event_id))
    db.session.delete(registration)
    db.session.commit()
    return Response("success", 204)

# todo Not sure if a sponsor has the privilege to remove a user's registration
def delete_sponsor_registration(payload):
    event_id = payload['event_id']
    user_id = payload['user_id']
    # todo comment for testing
    # event = Event.query.get_or_404(event_id)
    # if event.sponsor_id is not current_user.id:
    #     abort(403)
    registration = Registration.query.get_or_404((user_id, event_id))

    db.session.delete(registration)
    db.session.commit()
    return Response(200)

def delete_user_registration_ui(event_id):
    # registration = Registration.query.get_or_404({"user_id": current_user.id, "event_id": event_id})
    registration = Registration.query.get_or_404((current_user.id, event_id))
    db.session.delete(registration)
    db.session.commit()

    return redirect(url_for('main.home'))






def post_user_registration_ui(event_id):

    if current_user.is_anonymous:
        return Response('Please log in first', 403)
    if current_user.role.name == 'Sponsor':
        return Response('Please log in as User first', 403)

    event = Event.query.get_or_404(event_id)
    if Registration.query.get((current_user.id, event_id)):
        flash('Your have already been registered!', 'success')
#        return 'already registered', 400
    else:
        registration = Registration(user_id=current_user.id, event_id=event_id)
        db.session.add(registration)
        db.session.commit()

    flash('You have been registered to the event!', 'success')
    return redirect(url_for('main.home'))

#     registrers = Registration.query.filter_by(user_id=current_user.id).paginate(page=page, per_page=5)
#     return render_template('my_events.html', registrers=registrers)

