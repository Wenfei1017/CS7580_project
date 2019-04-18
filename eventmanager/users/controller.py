from eventmanager.users.model import User, RoleEnum
from eventmanager.users.forms import ResetPasswordForm, RequestResetForm, LoginForm, RegistrationForm, UpdateAccountForm
from flask_login import login_user, current_user, logout_user
from eventmanager import db, bcrypt, mail
from flask import Response, url_for, render_template, redirect, flash
from flask_mail import Message
import json


def obj_to_rep(obj):
    return {
        'id': obj.id,
        'username': obj.username,
        'email': obj.email,
        'role': obj.role.name
    }


def get_all_users():
    if current_user.is_anonymous or current_user.role.name == 'User':
        return Response('Method not allowed', 403)
    result = User.query.all()
    return json.dumps([obj_to_rep(r) for r in result])


def update_user(payload):
    if current_user.is_anonymous:
        return Response('Please log in first', 403)
    current_user.username = payload['username']
    current_user.email = payload['email']
    hashed_password = bcrypt.generate_password_hash(payload['password']).decode('utf-8')
    current_user.password = hashed_password
    db.session.commit()
    return Response('update user success', 200)


def delete_user_by_id(user_id):
    user = User.query.get_or_404(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return Response('delete user success', 200)


def create_user(payload):
    # import pdb; pdb.set_trace()
    if (not current_user.is_anonymous) and current_user.is_authenticated:
        return Response(f'already logged in by {current_user.username}', 400)
    if payload['role'] not in RoleEnum.__members__:
        return Response('role is incorrect, register failed', 400)
    if User.query.filter_by(username=payload['username']).first():
        return Response('username is taken, create user failed', 400)
    if User.query.filter_by(email=payload['email']).first():
        return Response('email is already registered', 400)
    hashed_password = bcrypt.generate_password_hash(payload['password']).decode('utf-8')
    # print(type(User.role))
    user = User(username=payload['username'], email=payload['email'], password=hashed_password, role=payload['role'])
    db.session.add(user)
    db.session.commit()
    return Response('register successful', 201)


def get_user_account():
    if current_user.is_anonymous:
        return Response('Please log in first', 403)
    return json.dumps(obj_to_rep(current_user))


def login(payload):
    if current_user.is_authenticated:
        return f'already logged in by {current_user.username}'
    user = User.query.filter_by(username=payload['username']).first()
    if user and bcrypt.check_password_hash(user.password, payload['password']):
        login_user(user)
        return Response('login successful', 200)
    else:
        return Response('login failed', 400)


def logout():
    logout_user()
    return Response('logout successful', 200)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='happyfive.eventmanager@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
        {url_for('users.reset_token', token=token, _external=True)}
        If you did not make this request then simply ignore this email and no changes will be made.
        '''
    mail.send(msg)


def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login_ui'))
    return render_template('reset_request.html', title='Reset Password', form=form)


def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_password'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login_ui'))
    return render_template('reset_token.html', title='Reset Password', form=form)


def login_ui(request):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


def logout_ui():
    logout_user()
    return redirect(url_for("main.home"))

def register_ui():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password,  role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login_ui'))
    return render_template('register.html', title='Register', form=form)


def account_ui(request):
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account_ui'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)