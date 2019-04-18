from flask import request, Blueprint
from flasgger.utils import swag_from
from eventmanager.users import controller
from flask_login import login_required

users = Blueprint('users', __name__)


# 'Content-Type': 'application/json'
# this route is only for testing
@users.route("/users", methods=['GET'])
def get_users():
    return controller.get_all_users()


@users.route("/users/register", methods=['POST'])
@swag_from('./swagger/register.yaml',  methods=['POST'])
def register():
    return controller.create_user(request.get_json())


@users.route("/users/account", methods=['GET'])
@swag_from('./swagger/account_get.yaml',  methods=['GET'])
def get_account():
    return controller.get_user_account()


@swag_from('./swagger/account_post.yaml',  methods=['PUT'])
@users.route("/users/account", methods=['PUT'])
def update_account():
    return controller.update_user(request.get_json())


@users.route("/users/login", methods=['POST'])
@swag_from('./swagger/login.yaml',  methods=['POST'])
def login():
    return controller.login(request.get_json())


@users.route("/users/logout", methods=['POST'])
@swag_from('./swagger/logout.yaml',  methods=['POST'])
def logout():
    return controller.logout()


@users.route("/users/reset_pw", methods=['GET', 'POST'])
def reset_password():
    return controller.reset_request()


@users.route("/users/reset_pw/<string:token>", methods=['GET', 'POST'])
def reset_token(token):
    return controller.reset_token(token)


@users.route("/login", methods=['GET', 'POST'])
def login_ui():
    return controller.login_ui(request)


@users.route("/logout")
def logout_ui():
    return controller.logout_ui()


@users.route("/register", methods=['GET', 'POST'])
def register_ui():
    return controller.register_ui()


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account_ui():
    return controller.account_ui(request)
