import json
from datetime import datetime

from flask import Response, abort, flash, redirect, url_for, render_template, request
from flask_login import current_user

from eventmanager import db
from eventmanager.events.model import Event, StatusEnum
from eventmanager.registrations.model import Registration, Rating
from eventmanager.reviews.forms import ReviewForm


def obj_to_rep(obj):
    return {
        'user_id': obj.user_id,
        'event_id': obj.event_id,
        'registration_time': str(obj.registration_time),
        'review_time': str(obj.review_time),
        'review_content': obj.review_content,
        'review_rating': obj.review_rating
    }


# Get all reviews, i.e. registrations with non-null review_time
# todo for testing only
def get_all_reviews():
    registrations = Registration.query.filter(Registration.review_time != None).all()
    return Response(json.dumps([obj_to_rep(rev) for rev in registrations]), 200, mimetype='application/json')


# Get a review (registration) by event's id and user id.
def get_one_review_by_review_keys(user_id, event_id):
    registration = Registration.query.get_or_404((user_id, event_id))
    if registration.review_time is None:
        return Response('Not reviewed yet', 404)
    else:
        return Response(json.dumps(obj_to_rep(registration)), 200, mimetype='application/json')


# Delete a review by review's key (event_id and user_id)
# This will make the registration's column of review attrs to be None.
def delete_review_by_review_keys(user_id, event_id):
    if current_user.is_anonymous:
        return Response('Please log in first', 403)
    if current_user.id != user_id:
        abort(403)
    registration = Registration.query.get_or_404((user_id, event_id))
    if registration.review_time is None:
        return Response('No review for this user in this event', 200)
    else:
        registration.review_time = None
        registration.review_rating = None
        registration.review_content = None
        db.session.commit()
        return Response('Delete review success', 200)


def create_review_ui(event_id):
    if current_user.is_anonymous:
        return Response('Please log in first', 403)
    if current_user.role.name == 'Sponsor':
        return Response('Please log in as User first', 403)
    form = ReviewForm()

    registration = Registration.query.get_or_404((current_user.id, event_id))
    event = Event.query.get_or_404(event_id)


    # rating choices in ReviewForm should be string to pass is_validated
    if form.validate_on_submit():
        if not registration:
            return Response('Please register the event first', 403)
        if event.time_end > datetime.utcnow():
            flash('Failed, Please wait until event finished', 'warning')
            return redirect(url_for('events.get_event', event_id=event_id))
            # return Response('Please wait until event finished', 403)
        registration.review_content = form.content.data
        registration.review_rating = Rating(int(form.rating.data))
        registration.review_time = form.review_time.data
        db.session.commit()
        flash('Your review has been posted!', 'success')
        return redirect(url_for('events.get_event_ui', event_id=event_id))
    elif request.method=='GET':
        if registration.review_time is not None:
            print(registration.review_rating.value)
            form.rating.data = str(registration.review_rating.value)
            form.content.data = registration.review_content

    return render_template('create_review.html', form=form, legend="Add/Edit Review to " + event.title)

# Create or update a review by review's key (event_id and user_id)
def update_review_by_review_keys(user_id, event_id, payload):
    if current_user.is_anonymous:
        return Response('Please log in first', 403)
    if current_user.id != user_id:
        abort(403)
    registration = Registration.query.get_or_404((user_id, event_id))

    registration.review_time = datetime.utcnow()
    registration.review_rating = Rating(int(payload.get('review_rating')))
    registration.review_content = payload.get('review_content')
    db.session.commit()
    return Response(json.dumps(obj_to_rep(registration)), 200, mimetype='application/json')


# Query all reviews. At least one of the filter(s): event_id., user_id not null.
# todo not sure if we should allow the user to query other use's registration
def query_all_reviews(request):
    if current_user.is_anonymous:
        return Response('Please log in first', 403)
    event_id = request.args.get('event', type=int)
    user_id = request.args.get('user', type=int)

    if event_id and user_id:
        registrations = Registration.query \
            .filter(Registration.event_id == event_id,
                    Registration.user_id == user_id,
                    Registration.review_time != None).all()
    elif event_id:
        registrations = Registration.query \
            .filter(Registration.event_id == event_id, Registration.review_time != None).all()
    elif user_id:
        registrations = Registration.query \
            .filter(Registration.user_id == user_id, Registration.review_time != None).all()
    else:
        return Response('query with at least one of user''s id or event''s id', 400)

    return Response(json.dumps([obj_to_rep(r) for r in registrations]), 200, mimetype='application/json')


# # Create a review of the event on behalf of the current user
# def create_review(payload):
#     review = Review(user_id=current_user.id,
#                     event_id=payload['event_id'],
#                     content=payload['content'],
#                     rating=payload['rating'])
#     db.session.add(review)
#     db.session.commit()
#     return Response('review created', 201)
#
#
# # Delete a review by review's id
# def delete_review_by_review_id(review_id):
#     review = Review.query.get_or_404(review_id)
#     if review:
#         db.session.delete(review)
#         db.session.commit()
#         return Response('Delete review success', 204)
#     return Response('Can not found review', 404)
#
#
# # Update a review (only allowed if the user is the author of the review)
# def update_review_by_review_id(payload):
#     review = Review.query.get_or_404(payload['review_id'])
#     if review.user != current_user:
#         abort(403)
#     else:
#         review.content = payload['content']
#         review.rating = payload['rating']
#         db.session.commit()
#         return Response('review updated', 200)
#
#
# # Get all the reviews of the current user
# def get_currentuser_all_reviews():
#     # print(current_user.reviews)
#     reviews = current_user.reviews
#     res = json.dumps([obj_to_rep(r) for r in reviews])
#     return Response(res, 200)
#
#
# # todo Delete all reviews of the user?
# def delete_user_all_reviews(user_id):
#     user = User.query.get_or_404(user_id)
#     if user:
#         reviews = user.reviews
#         if reviews:
#             for review in reviews:
#                 db.session.delete(review)
#             db.session.commit()
#             return Response(f"Delete all reviews of user (id='{user_id}')", 200)
#         return Response('No reviews', 200)
#     return Response('User not found', 404)
#
#
# # Get all the reviews by the id of an event ()
# # todo: not need to log in?
# def get_event_all_reviews(event_id):
#     event = Event.query.get_or_404(event_id)
#     reviews = event.reviews
#     res = json.dumps([obj_to_rep(review) for review in reviews])
#     return Response(res, 400)
