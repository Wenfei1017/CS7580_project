from flask import render_template, url_for, flash, redirect, request, Blueprint, Response, abort
from flask_login import login_required, current_user
from flasgger.utils import swag_from

from eventmanager import db
# from eventmanager.reviews.controller import *
from eventmanager.reviews import controller

reviews = Blueprint('reviews', __name__)


# todo test only
@reviews.route('/reviews/all', methods=['GET'])
def get_all_reviews():
    return controller.get_all_reviews()


# Get the review by review's composite keys (event_id and user_id)
@reviews.route("/events/<int:event_id>/users/<int:user_id>/review", methods=['GET'])
@swag_from('./swagger/get_review_by_id.yaml', methods=['GET'])
def get_review_by_id(event_id, user_id):
    return controller.get_one_review_by_review_keys(user_id, event_id)


# Update the review by review's composite keys (event_id and user_id)
# todo: for now only the author of the review can do changes to the review,
#  might allow some admin user to do this as well
@reviews.route("/events/<int:event_id>/users/<int:user_id>/review", methods=['PUT', 'POST'])
@swag_from('./swagger/put_review_by_id.yaml', methods=['PUT'])
@swag_from('./swagger/post_review_by_id.yaml', methods=['POST'])
def update_review_by_id(event_id, user_id):
    return controller.update_review_by_review_keys(user_id, event_id, request.get_json())


@reviews.route("/events/<int:event_id>/review/new", methods=['GET', 'POST'])
def create_review_ui(event_id):
    return controller.create_review_ui(event_id)



# Delete the review by review's composite keys (event_id and user_id)
# todo: for now only the author of the review can do changes to the review,
#  might allow some admin user to do this as well
@reviews.route("/events/<int:event_id>/users/<int:user_id>/review", methods=['DELETE'])
@swag_from('./swagger/del_review_by_id.yaml', methods=['DELETE'])
def delete_review_by_id(event_id, user_id):
    return controller.delete_review_by_review_keys(user_id, event_id)


# Query a list of review(s) using at least one of user_id or event_id.
# Use AND logic if both event_id and user_id is given.
@reviews.route("/reviews", methods=['GET'])
@swag_from('./swagger/query_review.yaml', methods=['GET'])
def query_reviews_by_event_and_or_user():
    return controller.query_all_reviews(request)
