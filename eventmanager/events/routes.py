from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, Response
from flasgger.utils import swag_from
from eventmanager.events import controller

events = Blueprint('events', __name__)


@events.route("/events", methods=['GET'])
@swag_from('./swagger/get_events.yaml',  methods=['GET'])
def get_events():
    return controller.get_all_events()


@events.route('/events/new', methods=['POST'])
@swag_from('./swagger/create_event.yaml', methods=['POST'])
def new_event():
    return controller.create_event(request.get_json())


@events.route("/events/<int:event_id>", methods=['GET','PUT','DELETE'])
@swag_from('./swagger/event_detail.yaml', methods=['GET'])
@swag_from('./swagger/event_delete.yaml', methods=['DELETE'])
@swag_from('./swagger/event_update.yaml', methods=['PUT'])
def get_event(event_id):
    #Todo: change back and add new
    if request.method == 'GET':
        return controller.event_detail(event_id)
    elif request.method == 'DELETE':
        return controller.event_delete(event_id)
    else:
        return controller.event_update(event_id, request.get_json())



@events.route("/events/<int:event_id>/detail", methods=['GET'])
def get_event_ui(event_id):
    return controller.event_detail_ui(event_id)



@events.route("/events/user/<int:user_id>", methods=['GET'])
@swag_from('./swagger/get_event_by_user_id.yaml', methods=['GET'])
def get_all_event_by_user_id(user_id):
    return controller.get_events_by_user_id(user_id)



@events.route("/events/status/<string:status>", methods=['GET'])
@swag_from('./swagger/get_event_by_status.yaml', methods=['GET'])
def get_all_event_by_status(status):
    return controller.get_event_by_status(status)


@events.route("/events/<string:category>", methods=['GET'])
@swag_from('./swagger/get_all_event_in_category.yaml', methods=['GET'])
def get_all_event_in_category(category):
    return controller.get_all_in_category(category)


@events.route("/search_ui", methods=['GET', 'POST'])
def search_events_ui():
    return controller.search_events_ui(request)


@events.route("/events/sort", methods=['GET'])
def sort_events():
    return controller.sort_events(request)


@events.route("/events/search", methods=['GET'])
def search_events():
    return controller.search_events(request)


@events.route("/events/create", methods=['GET','POST'])
def new_event_ui():
    return controller.new_event_ui()



@events.route("/events/<int:event_id>/delete", methods=['POST'])
def delete_event_ui(event_id):
    return controller.delete_my_event_ui(event_id)


@events.route("/events/update", methods=['GET','POST'])
def update_event_ui():
    return controller.my_event_update_ui(request)


@events.route("/events/latest", methods=['GET'])
def latest_event_ui():
    return controller.latest_event_ui(request)


@events.route("/announcement", methods=['GET'])
def announcement_ui():
    return controller.show_announcement_ui()

@events.route("/popular", methods=['GET'])
def popular_ui():
    return render_template('popular.html')

@events.route("/favoriate", methods=['GET'])
def favoriate_ui():
    return render_template('favoriate.html')


@events.route("/my_events", methods=['GET', 'POST'])
def my_events_ui():
    return controller.my_events_regis_ui(request)


@events.route("/events/near_me", methods=['GET'])
def near_event_ui():
    return controller.near_me_event_ui(request)

