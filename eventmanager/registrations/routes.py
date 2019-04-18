from flask import request, Blueprint
from flasgger.utils import swag_from
from eventmanager.registrations import controller

registrations = Blueprint('registrations', __name__)

'''GET
/registrations
sponsor: 403
user: all regi
/registrations?event=1
sponsor: all regi under event
user: the regi
/registrations?user=2
403
/registrations?event=1&user=2
sponsor: the regi
user: 403
'''


@registrations.route("/registrations", methods=['GET'])
@swag_from('./swagger/registrations_get.yaml', methods=['GET'])
def get_registration():
    return controller.get_registration(request)


@registrations.route("/registrations/new/<int:event_id>", methods=['POST'])
@swag_from('./swagger/registrations_new.yaml', methods=['POST'])
def create_registration_ui(event_id):
    return controller.post_user_registration_ui(event_id)


@registrations.route("/registrations", methods=['POST'])
@swag_from('./swagger/registrations_new.yaml', methods=['POST'])
def create_registration():
    return controller.post_user_registration(request.get_json())


@registrations.route("/registrations/delete/<int:event_id>", methods=['POST'])
@swag_from('./swagger/registrations_delete.yaml', methods=['POST'])
def delete_registration_ui(event_id):
    return controller.delete_registration_ui(event_id)


@registrations.route("/registrations", methods=['DELETE'])
@swag_from('./swagger/registrations_delete.yaml', methods=['DELETE'])
def delete_registration():
    return controller.delete_registration()

# @registrations.route("/myregistrations", methods=['GET', 'POST'])
# def create_registration_ui():
#     print("yyyyy")
#     print(request)
#     return controller.post_user_registration_ui(request)